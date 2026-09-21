# Railway Reservation System

An interactive, terminal-based railway reservation system built in Python (IDLE) with MySQL database connectivity. The project simulates end-to-end ticketing operations, including user registration, session authentication with CAPTCHA validation, train schedule queries, ticket booking, cancellation, and live PNR tracking.

---

## Features

### 1. User Management & Security
* **User Registration:** Secure signup capturing passenger credentials with 10-digit phone number validation.
* **Session Authentication:** Login verification validating credentials directly against stored MySQL records.
* **CAPTCHA Verification:** Dynamic 6-character alphanumeric CAPTCHA generation during signup and signin to prevent automated script submissions.

### 2. Train Operations & Search
* **Train Directory:** View all available trains with Train Number, Train Name, Route, and real-time seat availability.
* **Route Search:** Query trains based on specific Source and Destination stations.
* **Pre-seeded Routes:** Includes express routes such as Rajdhani Express, Shatabdi Express, and Duronto Express.

### 3. Ticketing Engine & Transactions
* **Seat Inventory Management:** Validates requested seats against available capacity and decrements seats automatically upon confirmation.
* **Payment Gateway Simulation:** Calculates total fare (₹500 per seat) with interactive user confirmation before issuing tickets.
* **Automated PNR Generation:** Generates a unique 10-character alphanumeric PNR code for every confirmed booking.

### 4. Booking Management & Cancellation
* **My Bookings:** Displays passenger booking history with route details fetched via relational SQL `JOIN` queries.
* **PNR Status Lookup:** Instant search to check booking and seat details for any issued PNR.
* **Ticket Cancellation & Restocking:** Deletes the booking record, calculates the refund amount, and increments seats back into the train inventory.

---

## Database Architecture

The application connects to MySQL via `mysql-connector-python` and automatically creates the `railway` database along with three relational tables:

users (User_Name [PK])
│
├──< bookings (Booking_ID [PK], User_Name [FK], Train_No [FK], PNR [UQ])
│
trains (Train_No [PK])

### Table Schemas

#### `users`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `User_Name` | VARCHAR(100) | PRIMARY KEY |
| `First_Name` | VARCHAR(100) | |
| `Last_Name` | VARCHAR(100) | |
| `Password` | VARCHAR(50) | |
| `Email_Id` | VARCHAR(50) | |
| `Phone_No` | VARCHAR(20) | |

#### `trains`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `Train_No` | INT | PRIMARY KEY |
| `Train_Name` | VARCHAR(100) | |
| `Source` | VARCHAR(100) | |
| `Destination` | VARCHAR(100) | |
| `Seats_Available` | INT | |

#### `bookings`
| Column | Type | Constraints |
| :--- | :--- | :--- |
| `Booking_ID` | INT | AUTO_INCREMENT, PRIMARY KEY |
| `User_Name` | VARCHAR(100) | FOREIGN KEY -> `users(User_Name)` |
| `Train_No` | INT | FOREIGN KEY -> `trains(Train_No)` |
| `Seats_Booked` | INT | |
| `PNR` | VARCHAR(10) | UNIQUE |
| `Booking_Time` | DATETIME | DEFAULT CURRENT_TIMESTAMP |

---

## Prerequisites

* **Python:** Version 3.8 or higher
* **MySQL Server:** Version 5.7 or 8.0
* **Python Connector:** `mysql-connector-python`
* **Development Environment:** Python IDLE or any compatible terminal

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/vikrantkumar24/railway-reservation-system.git](https://github.com/vikrantkumar24/railway-reservation-system.git)
cd railway-reservation-system
2. Install Dependencies
Bash
pip install mysql-connector-python
3. Ensure MySQL Server is Running
Make sure your local MySQL service is running. The script executes CREATE DATABASE IF NOT EXISTS railway and initializes the tables automatically upon connection.

4. Run the Application
Open the file in Python IDLE or run it via terminal:

Bash
python railway_reservation.py
When prompted, enter your MySQL root password to complete the initial setup.

Portal Navigation Flow
Plaintext
+=============================================+
|    WELCOME TO RAILWAY RESERVATION PORTAL    |
+=============================================+
|  [1] Sign In                                |
|  [2] Sign Up                                |
|  [Q] Quit                                   |
+=============================================+
                      │
                      ▼ (Upon Successful Login)
+=============================================+
|              RAILWAY SERVICES               |
+=============================================+
|  [1] View All Trains                        |
|  [2] Search Train by Route                  |
|  [3] Book Ticket                            |
|  [4] My Bookings                            |
|  [5] PNR Status                             |
|  [6] Cancel Ticket                          |
|  [7] Logout                                 |
+=============================================+
Limitations
Plaintext Storage: Passwords are currently stored in plaintext without cryptographic hashing.

Sequential Execution: Designed as a single-user CLI application; does not handle concurrent multi-user database transactions.

Flat Fare Model: Uses a fixed price model (₹500/seat) rather than distance or class-based dynamic fare calculations.

Author
Vikrant Kumar

Developed as an academic Computer Science project in Python & MySQL.
