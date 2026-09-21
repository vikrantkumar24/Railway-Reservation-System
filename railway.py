
######################### MODULES ##############################

import mysql.connector as sqltor
import random

######################### DB CONNECTIONS ##############################

passwrd = str(input("Enter Database Password: "))
myconn = sqltor.MySQLConnection(host="localhost", user="root", password=passwrd)
myconn.autocommit = True
cursor = myconn.cursor()

######################### DB & TABLE CREATIONS ##############################

cursor.execute("CREATE DATABASE IF NOT EXISTS railway")
cursor.execute("USE railway")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        User_Name VARCHAR(100) PRIMARY KEY,
        First_Name VARCHAR(100),
        Last_Name VARCHAR(100),
        Password VARCHAR(50),
        Email_Id VARCHAR(50),
        Phone_No VARCHAR(20)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS trains (
        Train_No INT PRIMARY KEY,
        Train_Name VARCHAR(100),
        Source VARCHAR(100),
        Destination VARCHAR(100),
        Seats_Available INT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        Booking_ID INT AUTO_INCREMENT PRIMARY KEY,
        User_Name VARCHAR(100),
        Train_No INT,
        Seats_Booked INT,
        PNR VARCHAR(10) UNIQUE,
        Booking_Time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (User_Name) REFERENCES users(User_Name),
        FOREIGN KEY (Train_No) REFERENCES trains(Train_No)
    )
""")

######################## TRAINS DETAILS ########################

trains = [
    (1001, "Rajdhani Express", "Delhi", "Mumbai", 100),
    (1002, "Shatabdi Express", "Delhi", "Chandigarh", 75),
    (1003, "Duronto Express", "Mumbai", "Kolkata", 50)
]
for train in trains:
    cursor.execute("INSERT IGNORE INTO trains VALUES (%s, %s, %s, %s, %s)", train)

print("✅ Database setup complete.")

######################## INTERNAL FUNCTIONS ########################

def validate_phone_no(phone_number):
    cleaned_no = phone_number.strip().replace("-","").replace(" ","")
    check_ten_digits = len(cleaned_no) == 10
    digits = cleaned_no.isdigit()
    return check_ten_digits and digits

def check_no(no):
    valid = validate_phone_no(no)
    if valid:
        print()
    else:
        global Phone_Number_Error
        Phone_Number_Error = 1
        print()

def generate_captcha(length=6):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def verify_captcha():
    captcha = generate_captcha()
    print("\nCaptcha:", captcha)
    user_input = input("Enter the captcha as shown above: ").strip()
    if user_input == captcha:
        print("✅ Captcha verified!")
        return True
    else:
        print("❌ Incorrect captcha.")
        return False

def generate_pnr():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

def payment_gateway(amount):
    print(f"\n💳 Payment Gateway: Amount to pay ₹{amount}")
    confirm = input("Proceed with payment? (yes/no): ").lower()
    if confirm == "yes":
        print("Processing payment...")
        print("✅ Payment successful!")
        return True
    else:
        print("❌ Payment cancelled.")
        return False

######################## MAIN FUNCTIONS ########################
def SignUp():
    while True:
        global Phone_Number_Error
        Phone_Number_Error = 0
        width = 45
        line = "=" * width

        print("+" + line + "+") 
        print("|" + " SIGN UP PAGE ".center(width) + "|") 
        print("+" + line + "+")

        print()
        print("Type 'quit' as the username to leave the sign-up page.")
        print()
        
        user_name = input("Username: ")

        if user_name.lower() == "quit":
            print("Exiting Into Sign In Page!")
            break
        
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = input("Password: ")
        email_id = input("Email: ")
        phone_no = (input("Phone Number: "))

        check_no(phone_no)

        if Phone_Number_Error == 1:
            print("❌ Invalid Phone Number, Try Again!")
            print()
            continue
        else:
            if not verify_captcha():
                print("❌ Incorrect captcha.")
                print()
                continue

            command = """INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (user_name, first_name, last_name, password, email_id, phone_no)
            try:
                cursor.execute(command, values)
                print()
                print("✅ Account created successfully!")
                break
            
            except sqltor.errors.IntegrityError:
                print("❌ Data Entry Error!")
                print()
                continue

    
def SignIn():
    while True:
        width = 45
        line = "=" * width

        print("+" + line + "+") 
        print("|" + " SIGN IN PAGE ".center(width) + "|") 
        print("+" + line + "+")

        print()
        print("Type 'quit' as the username to leave the sign-in page.")
        print()
        
        user_name = input("Username: ")

        if user_name.lower() == "quit":
            print("Exit Into Sign In Page!")
            break
        
        password = input("Password: ")
    
        if not verify_captcha():
            print("❌ Incorrect captcha.")
            print()
            continue

        cursor.execute("SELECT * FROM users WHERE User_Name = %s AND Password = %s", (user_name, password))
        record = cursor.fetchone()
    
        if record:
            print()
            width = 47
            line = "=" * width

            print("+" + line + "+") 
            print("|" +f" ✅ Welcome back, {record[1]} {record[2]}! ".center(width - 1) + "|") 
            print("+" + line + "+")
            print()
            railway_services(user_name)
            break
        else:
            print("❌ Invalid username or password.")
            continue

def view_trains():
    cursor.execute("SELECT * FROM trains")
    rows = cursor.fetchall()
    print(f"{'Train No':<10} {'Train Name':<20} {'Route':<25} {'Seats':<5}")
    print("-" * 65)
    
    for train in trains:
        route = f"{train[2]} → {train[3]}"
        print(f"{train[0]:<10} {train[1]:<20} {route:<25} {train[4]:<5}")

    print()


def search_trains():
    source = input("Enter Source: ")
    destination = input("Enter Destination: ")
    cursor.execute("SELECT * FROM trains WHERE Source = %s AND Destination = %s", (source, destination))
    results = cursor.fetchall()
    if results:
        print("\nMatching Trains:")
        for train in results:
            print(f"{train[0]} | {train[1]} | Seats: {train[4]}")
        print()
    else:
        print("❌ No trains found.")

def book_ticket(user_name):
    train_no = int(input("Enter Train No: "))
    seats = int(input("Seats to book: "))
    cursor.execute("SELECT Train_Name, Seats_Available FROM trains WHERE Train_No = %s", (train_no,))
    train = cursor.fetchone()
    if not train or train[1] < seats:
        print("❌ Train not found or insufficient seats.")
        return
    fare = seats * 500
    if payment_gateway(fare):
        pnr = generate_pnr()
        cursor.execute("""
            INSERT INTO bookings (User_Name, Train_No, Seats_Booked, PNR)
            VALUES (%s, %s, %s, %s)
        """, (user_name, train_no, seats, pnr))
        cursor.execute("UPDATE trains SET Seats_Available = Seats_Available - %s WHERE Train_No = %s", (seats, train_no))
        myconn.commit()
        print()
        print(f"🎫 Ticket booked. Your PNR: {pnr}")
        print()
    else:
        print("❌ Payment failed. Booking cancelled.")
        print()

def view_bookings(user_name):
    cursor.execute("""
        SELECT b.Booking_ID, b.PNR, t.Train_Name, t.Source, t.Destination, b.Seats_Booked, b.Booking_Time
        FROM bookings b JOIN trains t ON b.Train_No = t.Train_No
        WHERE b.User_Name = %s
    """, (user_name,))
    rows = cursor.fetchall()
    print()
    if rows:
        print(f"{'Booking ID':<12} {'PNR':<12} {'Train':<20} {'From':<12} {'To':<15} {'Seats':<6} {'Time'}")
        print("-" * 90)
        for b in rows:
            print(f"{b[0]:<12} {b[1]:<12} {b[2]:<20} {b[3]:<12} {b[4]:<15} {b[5]:<6} {b[6]}")
        print()
    else:
        print("No bookings found.")
        print()

def pnr_status():
    pnr = input("Enter your PNR: ").strip().upper()
    cursor.execute("""
        SELECT b.PNR, t.Train_Name, t.Source, t.Destination, b.Seats_Booked, b.Booking_Time 
        FROM bookings b
        JOIN trains t ON b.Train_No = t.Train_No
        WHERE b.PNR = %s
    """, (pnr,))
    result = cursor.fetchone()
    if result:
        print("\n📄 PNR Status:")
        print(f"PNR: {result[0]}, Train: {result[1]}, From: {result[2]}, To: {result[3]}, Seats: {result[4]}, Time: {result[5]}")
        print()
    else:
        print("❌ Invalid PNR.")
        print()

def cancel_ticket(user_name):
    pnr = input("Enter PNR to cancel: ").strip().upper()
    cursor.execute("SELECT Train_No, Seats_Booked FROM bookings WHERE PNR = %s AND User_Name = %s", (pnr, user_name))
    result = cursor.fetchone()
    if not result:
        print("❌ Booking not found or not yours.")
        return
    train_no, seats = result
    refund = seats * 500
    confirm = input(f"Confirm cancel? Refund ₹{refund} (yes/no): ").lower()
    if confirm == "yes":
        cursor.execute("DELETE FROM bookings WHERE PNR = %s", (pnr,))
        cursor.execute("UPDATE trains SET Seats_Available = Seats_Available + %s WHERE Train_No = %s", (seats, train_no))
        myconn.commit()
        print()
        print(f"✅ Cancelled Sucessfully. Refund ₹{refund}")
        print()
    else:
        print()
        print("❌ Cancel aborted.")
        print()

def railway_services(user_name):
    while True:
        width = 45
        line = "=" * width

        print("+" + line + "+") 
        print("|" + " RAILWAY SERVICES ".center(width) + "|") 
        print("+" + line + "+")
        print("|" + "[1] View All Trains      ".center(width) + "|")
        print("|" + "[2] Search Train by Route".center(width) + "|")
        print("|" + "[3] Book Ticket          ".center(width) + "|")
        print("|" + "[4] My Bookings          ".center(width) + "|")
        print("|" + "[5] PNR Status           ".center(width) + "|")
        print("|" + "[6] Cancel Ticket        ".center(width) + "|")
        print("|" + "[7] Logout               ".center(width) + "|")
        print("+" + line + "+")

        print()
        
        choice = input("Choose The Option: ")
        if choice == "1":
            view_trains()
        elif choice == "2":
            search_trains()
        elif choice == "3":
            book_ticket(user_name)
        elif choice == "4":
            view_bookings(user_name)
        elif choice == "5":
            pnr_status()
        elif choice == "6":
            cancel_ticket(user_name)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("❌ Invalid option.")

# ========== Main Program ==========

while True:
    try:
        width = 45
        line = "=" * width

        print("+" + line + "+") 
        print("|" + " WELCOME TO RAILWAY RESERVATION PORTAL ".center(width) + "|") 
        print("+" + line + "+")

        print("|" + "[1] Sign In".center(width) + "|")
        print("|" + "[2] Sign Up".center(width) + "|")
        print("|" + "[Q] Quit   ".center(width) + "|")

        print("+" + line + "+")

        print()

        option = input("Choose option: ").lower()
        if option == "1":
            print()
            SignIn()
        elif option == "2":
            print()
            SignUp()
        elif option == "q":
            print("You have exited the portal. Goodbye!")
            break
        else:
            print("❌ Invalid Option. Try again.")
            
    except ValueError:
        print("❌ Invalid input. Try again.")
        continue
