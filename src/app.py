from flask import Flask, render_template, request, jsonify
import psycopg2
import pandas as pd
import os
import config #Used and in .gitignore, so we can work on different databases.

app = Flask(__name__)

# Database configuration
DB_NAME = config.DB_NAME    #'your_db_name'
DB_USER = config.DB_USER    #'your_db_user'
DB_PASS = config.DB_PASS    #'your_db_password'
DB_HOST = config.DB_HOST    #'your_db_host'
DB_PORT = config.DB_PORT    #'your_db_port'

# set your own database name, username and password
db = "dbname='Crypto' user='postgres' host='localhost' password='Krelle2024'" #potentially wrong password
conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
