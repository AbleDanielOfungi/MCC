import sqlite3

def create_league_table():
    conn = sqlite3.connect('database.db')  # Replace with your actual database name
    conn.execute('''
        CREATE TABLE IF NOT EXISTS league_table (
            team_id INTEGER PRIMARY KEY,
            matches_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            draws INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            goal_difference INTEGER DEFAULT 0,
            goals_scored INTEGER DEFAULT 0,
            goals_conceded INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("league_table has been created.")

# Call the function to create the table
create_league_table()
