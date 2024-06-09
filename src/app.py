from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import psycopg2
import pandas as pd
import os
import config       #Used and in .gitignore, so we can work on different databases.
import re           #regex

app = Flask(__name__)

# Database configuration (from config.py)
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

#Frontpage
@app.route('/')
def index():
    cursor.execute('SELECT gameId, title FROM games ORDER BY random() LIMIT 100')
    games = cursor.fetchall()
    
    # Fetch distinct values for dropdowns
    cursor.execute('SELECT DISTINCT genre FROM games')
    genres = cursor.fetchall()
    cursor.execute('SELECT DISTINCT developer FROM games')
    developers = cursor.fetchall()
    cursor.execute('SELECT DISTINCT releaseyear FROM games ORDER BY releaseyear')
    releaseyears = cursor.fetchall()

    cursor.execute('SELECT platform_id, platform_name FROM Platforms ORDER BY platform_name')
    platform_names = cursor.fetchall()

    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html', games=games, genres=genres, developers=developers, releaseyears=releaseyears, platforms=platform_names)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        genre_filter = request.form.get('genre', '')
        developer_filter = request.form.get('developer', '')
        releaseyear_filter = request.form.get('releaseyear', '')
        platform_filter = request.form.get('platform', '')

        query = "SELECT gameId, title FROM games WHERE title ILIKE %s"
        params = ['%' + search_query + '%']

        if genre_filter:
            query += " AND genre = %s"
            params.append(genre_filter)
        if developer_filter:
            query += " AND developer = %s"
            params.append(developer_filter)
        if releaseyear_filter:
            query += " AND releaseyear = %s"
            params.append(releaseyear_filter)
        if platform_filter:
           query += " AND gameId IN (SELECT gameId FROM GamePlatforms WHERE platform_id = %s)"
           params.append(platform_filter)


        cursor.execute(query, params)
        games = cursor.fetchall()
        
        # Fetch distinct values for dropdowns
        cursor.execute('SELECT DISTINCT genre FROM games')
        genres = cursor.fetchall()
        cursor.execute('SELECT DISTINCT developer FROM games')
        developers = cursor.fetchall()
        cursor.execute('SELECT DISTINCT releaseyear FROM games ORDER BY releaseyear')
        releaseyears = cursor.fetchall()

        cursor.execute('SELECT platform_id, platform_name FROM Platforms ORDER BY platform_name')
        platform= cursor.fetchall()

        return render_template('index.html', games=games, genres=genres, developers=developers, releaseyears=releaseyears, search_query=search_query, genre_filter=genre_filter, developer_filter=developer_filter, releaseyear_filter=releaseyear_filter, platforms=platform)
    return redirect(url_for('index'))


#When clicking on a game, presumably from the frontpage but can be used elsewhere if needed.
@app.route('/game/<gameId>')
def game_detail(gameId):
    if not session.get('logged_in'):
        return render_template('login.html')
    
    cursor.execute('SELECT title, genre, developer, releaseyear FROM games WHERE gameId = %s', (gameId,))
    game = cursor.fetchone()
    cursor.execute(f'''SELECT * FROM reviews where gameid = '{gameId}' ORDER BY random()''')   #review test
    allreviews = cursor.fetchall()                                                              #review test
    average = 0
    if len(allreviews)>0:
        sum = 0
        for i in range(0,len(allreviews)):
            sum = sum + allreviews[i][2]
        average = round(sum/len(allreviews),1)
    reviews = allreviews[:5]
    if game:
        return render_template('game_detail.html', game=game, gameId=gameId, reviews=reviews, average=average)
    else:
        return "Game not found", 404

@app.route('/submit_review/<gameId>', methods=['POST'])
def submit_review(gameId):
    if not session.get('logged_in'):
        return render_template('login.html')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    username = session.get('username')  # Retrieve username from session
    
    if rating and comment and username:
        cur = conn.cursor()
        # Check if a review by this user for this game already exists
        cur.execute('SELECT * FROM Reviews WHERE gameId = %s AND username = %s', (gameId, username))
        existing_review = cur.fetchone()
        
        if existing_review:
            # Update the existing review
            cur.execute('UPDATE Reviews SET review_score = %s, comment = %s WHERE gameId = %s AND username = %s', 
                        (rating, comment, gameId, username))
        else:
            # Insert a new review
            cur.execute('INSERT INTO Reviews (gameId, username, review_score, comment) VALUES (%s, %s, %s, %s)', 
                        (gameId, username, rating, comment))
        
        conn.commit()
        cur.close()
        
    return redirect(url_for('game_detail', gameId=gameId))

@app.route('/profile')
def profile():
    username = session.get('username')  # Retrieve username from session
    if not session.get('logged_in'):
        return render_template('login.html')
    
    cur = conn.cursor()
    cur.execute('''
        SELECT Reviews.gameId, Games.title, Reviews.review_score, Reviews.comment
        FROM Reviews
        JOIN Games ON Reviews.gameId = Games.gameId
        WHERE Reviews.username = %s
        ORDER BY Reviews.review_score DESC
    ''', (username,))
    reviews = cur.fetchall()
    cur.close()
    
    return render_template('profile.html', username=username, reviews=reviews)


#logout button.
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('login.html')

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
                    return redirect(url_for("index"))
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

    cur.execute(f''' SELECT * from users where username = '{username}' and password = '{password}' ''')

    if len(cur.fetchall()) != 0:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('Wrong password!')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)


