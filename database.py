import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "travel_customers.db"


# Connect to database
def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ==================================
# 1. CREATE TABLE
# ==================================

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT,

            destination TEXT NOT NULL,

            days INTEGER,

            budget TEXT,

            interests TEXT,

            itinerary TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


# ==================================
# 2. ADD CUSTOMER
# ==================================

def add_customer(
    name,
    email,
    destination,
    days,
    budget,
    interests,
    itinerary
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO customers (
            name,
            email,
            destination,
            days,
            budget,
            interests,
            itinerary
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (
        name,
        email,
        destination,
        days,
        budget,
        ", ".join(interests),
        itinerary
    ))

    conn.commit()

    customer_id = cursor.lastrowid

    conn.close()

    return customer_id


# ==================================
# 3. GET CUSTOMERS
# ==================================

def get_customers():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM customers
        ORDER BY id DESC
    """)

    customers = cursor.fetchall()

    conn.close()

    return customers


# ==================================
# 4. SEARCH CUSTOMER
# ==================================

def search_customer(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM customers

        WHERE name LIKE ?
        OR email LIKE ?
        OR destination LIKE ?

    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    customers = cursor.fetchall()

    conn.close()

    return customers


# ==================================
# 5. UPDATE CUSTOMER
# ==================================

def update_customer(
    customer_id,
    name,
    email,
    destination,
    days,
    budget
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE customers

        SET name = ?,
            email = ?,
            destination = ?,
            days = ?,
            budget = ?

        WHERE id = ?

    """, (
        name,
        email,
        destination,
        days,
        budget,
        customer_id
    ))

    conn.commit()
    conn.close()


# ==================================
# 6. DELETE CUSTOMER
# ==================================

def delete_customer(customer_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM customers
        WHERE id = ?
    """, (customer_id,))

    conn.commit()
    conn.close()