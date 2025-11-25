import sqlite3
import os

# Path to the local database file
DB_PATH = os.path.join(os.path.dirname(__file__), "workshop.db")


def initialize_local_db():
    """
    Creates the necessary tables in SQLite if they do not exist.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Table: Local Stock
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS local_stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                category TEXT,
                purchase_price REAL,
                selling_price REAL,
                qty INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # 2. Table: Job Cards
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS local_jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                vehicle_number TEXT,
                mobile_no TEXT,
                service_type TEXT,
                status TEXT,
                entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()
        print(f"SUCCESS: Local Database checked at {DB_PATH}")
    except Exception as e:
        print(f"ERROR: Failed to init Local DB: {e}")
