from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

    #index route
@app.route('/')
def index():
    conn = get_db_connection()
    league_table = conn.execute('''
        SELECT t.name AS team_name, lt.matches_played, lt.wins, lt.draws, lt.losses, lt.goals_scored AS GF, lt.goals_conceded AS GA, 
               lt.goal_difference, lt.points
        FROM league_table lt
        JOIN teams t ON lt.team_id = t.id
        ORDER BY lt.points DESC, lt.goal_difference DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', league_table=league_table)


# add result route
import re

@app.route('/add_result', methods=['POST'])
def add_result():
    team1 = request.form['team1']
    team2 = request.form['team2']
    goals_team1 = request.form['goals_team1']
    goals_team2 = request.form['goals_team2']

    # Validate that the goal scores are non-negative integers
    if not (goals_team1.isdigit() and goals_team2.isdigit()):
        return "Error: Goal scores must be non-negative integers.", 400

    goals_team1 = int(goals_team1)
    goals_team2 = int(goals_team2)

    # Ensure that team names are not the same
    if team1.lower() == team2.lower():
        return "Error: A team cannot play against itself.", 400

    conn = get_db_connection()

    # Check if teams exist, if not insert them into the teams table
    for team in [team1, team2]:
        existing_team = conn.execute('SELECT id FROM teams WHERE LOWER(name) = ?', (team.lower(),)).fetchone()
        if not existing_team:
            conn.execute('INSERT INTO teams (name) VALUES (?)', (team,))
    
    # Fetch team IDs for further processing
    team1_id = conn.execute('SELECT id FROM teams WHERE LOWER(name) = ?', (team1.lower(),)).fetchone()['id']
    team2_id = conn.execute('SELECT id FROM teams WHERE LOWER(name) = ?', (team2.lower(),)).fetchone()['id']

    # Update league table with the results
    update_league_table(conn, team1_id, goals_team1, goals_team2)
    update_league_table(conn, team2_id, goals_team2, goals_team1)

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# update league table
def update_league_table(conn, team_id, goals_scored, goals_conceded):
    team_stats = conn.execute('SELECT * FROM league_table WHERE team_id = ?', (team_id,)).fetchone()

    if not team_stats:
        team_stats = {
            'matches_played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'points': 0,
            'goal_difference': 0,
            'goals_scored': 0,
            'goals_conceded': 0
        }

    matches_played = team_stats['matches_played'] + 1
    goals_scored_total = team_stats['goals_scored'] + goals_scored
    goals_conceded_total = team_stats['goals_conceded'] + goals_conceded
    goal_difference = goals_scored_total - goals_conceded_total

    if goals_scored > goals_conceded:
        wins = team_stats['wins'] + 1
        draws = team_stats['draws']
        losses = team_stats['losses']
        points = team_stats['points'] + 3
    elif goals_scored == goals_conceded:
        wins = team_stats['wins']
        draws = team_stats['draws'] + 1
        losses = team_stats['losses']
        points = team_stats['points'] + 1
    else:
        wins = team_stats['wins']
        draws = team_stats['draws']
        losses = team_stats['losses'] + 1
        points = team_stats['points']

    if team_stats['matches_played'] == 0:
        conn.execute('''
            INSERT INTO league_table (team_id, matches_played, wins, draws, losses, points, goal_difference, goals_scored, goals_conceded)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (team_id, matches_played, wins, draws, losses, points, goal_difference, goals_scored_total, goals_conceded_total))
    else:
        conn.execute('''
            UPDATE league_table
            SET matches_played = ?, wins = ?, draws = ?, losses = ?, points = ?, goal_difference = ?, goals_scored = ?, goals_conceded = ?
            WHERE team_id = ?
        ''', (matches_played, wins, draws, losses, points, goal_difference, goals_scored_total, goals_conceded_total, team_id))

if __name__ == '__main__':
    app.run(debug=True)
