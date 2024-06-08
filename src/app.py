from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import psycopg2
import pandas as pd
import os
import config       #Used and in .gitignore, so we can work on different databases.
import re           #regex

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
    cursor.execute('SELECT id, title FROM games order by random() LIMIT 10')
    games = cursor.fetchall()
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html', games=games)


@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cursor = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_mail = request.form['mail']
        new_password = request.form['password']
        cursor.execute(f'''SELECT * FROM users where username = '{new_username}' ''')
        unique_username = cursor.fetchall()
        
        cursor.execute(f'''SELECT * from users where mail = '{new_mail}' ''')
        unique_mail = cursor.fetchall()
        flash('Account created!')
        if len(unique_username) == 0:
            if  len(unique_mail) == 0:
                mail_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  #Regex pattern for a mail
                if re.match(mail_pattern, new_mail):
                    cursor.execute(f'''INSERT INTO users(username, password, mail) VALUES ('{new_username}', '{new_password}', '{new_mail}')''')
                    flash('Account created!')
                    conn.commit()
                    return redirect(url_for("index")) #replace later
                else:
                    flash('Invalid mail!')
            else: 
                flash('Mail already exists!')
        else: 
            flash('Username already exists!')
    return render_template("createaccount.html")

@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password'] 

    insys = f''' SELECT * from users where username = '{username}' and password = '{password}' '''

    cur.execute(insys)

    ifcool = len(cur.fetchall()) != 0

    if ifcool:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('Wrong password!')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
