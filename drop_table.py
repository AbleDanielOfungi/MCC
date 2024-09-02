import sqlite3

def drop_league_table():
    conn = sqlite3.connect('database.db')  # Replace with your actual database name
    conn.execute('DROP TABLE IF EXISTS league_table')
    conn.commit()
    conn.close()
    print("league_table has been dropped.")

# Call the function to drop the table
drop_league_table()
