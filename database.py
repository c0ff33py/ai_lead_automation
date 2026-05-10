import sqlite3

def save_lead(name, phone, business_type):

    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        business_type TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO leads (name, phone, business_type)
    VALUES (?, ?, ?)
    """, (name, phone, business_type))

    conn.commit()
    conn.close()