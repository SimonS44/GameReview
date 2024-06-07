from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import psycopg2
import pandas as pd
import os
import config #Used and in .gitignore, so we can work on different databases.
import re #regex

app = Flask(__name__)

# Database configuration
DB_NAME = config.DB_NAME    #'your_db_name'
DB_USER = config.DB_USER    #'your_db_user'
DB_PASS = config.DB_PASS    #'your_db_password'
DB_HOST = config.DB_HOST    #'your_db_host'
DB_PORT = config.DB_PORT    #'your_db_port'

# set your own database name, username and password
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


@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_mail = request.form['mail']
        new_password = request.form['password']
        cur.execute(f'''select * from users where username = '{new_username}' ''')
        cur.execute(f'''select * from users where mail = '{new_mail}' ''')
        unique = cur.fetchall()
        flash('Account created!')
        if  len(unique) == 0:
            mail_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if re.match(mail_pattern, new_mail):
                cur.execute(f'''INSERT INTO users(username, password, mail) VALUES ('{new_username}', '{new_password}'), '{new_mail}')''')
                flash('Account created!')
                conn.commit()

                return redirect(url_for("home"))
            else:
                flash('mail address error')
        else: 
            flash('Username or mail already exists!')


    return render_template("createaccount.html")


if __name__ == '__main__':
    app.run(debug=True)
