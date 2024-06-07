from flask import Flask, render_template, request, jsonify
import psycopg2
import pandas as pd
import os
import config

app = Flask(__name__)

# Database configuration
DB_NAME = config.DB_NAME#'your_db_name'
DB_USER = config.DB_USER#'your_db_user'
DB_PASS = config.DB_PASS#'your_db_password'
DB_HOST = config.DB_HOST#'your_db_host'
DB_PORT = config.DB_PORT#'your_db_port'

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games', methods=['GET'])
def get_games():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM games;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/add_game', methods=['POST'])
def add_game():
    new_game = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO games (name, genre, rating) VALUES (%s, %s, %s);',
        (new_game['name'], new_game['genre'], new_game['rating'])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'Game added'}), 201

if __name__ == '__main__':
    app.run(debug=True)
