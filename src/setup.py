import config       #Used and in .gitignore, so we can work on different databases.
import psycopg2
import os


#base_path = os.path.abspath(os.getcwd()) #replace with your path if it does not work\GameReview
try:
     
    base_path = os.path.normpath(os.getcwd())
    x = base_path[len(base_path)-10:]
    print(x)
    if x != 'GameReview':
        base_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
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
    create_tables_query = '''
    --Games
    DROP TABLE Games CASCADE; 	        --remove / outcomment if first time running code.
    DROP TABLE users; 	                --remove / outcomment if first time running code.
    DROP TABLE reviews;	                --remove / outcomment if first time running code.
    DROP TABLE Platforms CASCADE;       --remove / outcomment if first time running code.
    DROP TABLE GamePlatforms;           --remove / outcomment if first time running code.

    CREATE TABLE IF NOT EXISTS Games(
        gameId char(3),
        title char(50),
        genre char(50),
        developer char(50),
        releaseyear char(4),
        CONSTRAINT games_pk PRIMARY KEY (gameId)
    );
    --Import games
    COPY Games(gameId, title, genre, developer, releaseyear)
    FROM %s
    DELIMITER ','
    CSV HEADER;

    --Users
    CREATE TABLE IF NOT EXISTS users(
        username char(20) NOT NULL,
        mail char(100) NOT NULL,
        password char(20) NOT NULL,
        CONSTRAINT user_pk PRIMARY KEY (username)
    );

    INSERT INTO users(username, mail, password) VALUES ('q', 'q@q.q', 'q'); -- Default user for testing.

    --Reviews
    CREATE TABLE IF NOT EXISTS Reviews(
        gameId char(4) NOT NULL,
        username char(20) NOT NULL,
        review_score int NOT NULL,
        comment char(300),
        CONSTRAINT review_pk PRIMARY KEY (gameId, username)
    );
    --Import reviews
    COPY Reviews(gameId, username, review_score, comment)
    FROM %s
    DELIMITER ','
    CSV HEADER;

    CREATE TABLE IF NOT EXISTS Platforms(
    platform_id char(2) NOT NULL,
    platform_name VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT platforms_pk PRIMARY KEY (platform_id)
    );

    COPY Platforms(platform_id, platform_name)
    FROM %s
    DELIMITER ','
    CSV HEADER;

    CREATE TABLE IF NOT EXISTS GamePlatforms(
    gameId CHAR(3) NOT NULL,
    platform_id char(2) NOT NULL,
    CONSTRAINT fk_game FOREIGN KEY (gameId) REFERENCES Games(gameId) ON DELETE CASCADE,
    CONSTRAINT fk_platform FOREIGN KEY (platform_id) REFERENCES Platforms(platform_id) ON DELETE CASCADE,
    CONSTRAINT pk_game_platform PRIMARY KEY (gameId, platform_id)
    );

    COPY GamePlatforms(gameId, platform_id)
    FROM %s
    CSV HEADER;
    '''

    copy_query = create_tables_query % (f"'{base_path}/tmp/games.csv'", f"'{base_path}/tmp/Reviews.csv'", f"'{base_path}/tmp/Platforms.csv'", f"'{base_path}/tmp/GamePlatforms.csv'")

    cursor.execute(copy_query)
    conn.commit()

    cursor.close()
    conn.close()
    print("Done!")
except:
    print("error dir is wack")
