import sqlite3

def list_tables():
    conn = sqlite3.connect('database.db')  # Replace with your database name
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

    conn.close()

# Call the function to list tables
list_tables()
