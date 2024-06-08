DROP TABLE Games; 	--remove / outcomment if first time running code.
DROP TABLE users; 	--remove / outcomment if first time running code.
DROP TABLE reviews;	--remove / outcomment if first time running code.
--Games
CREATE TABLE IF NOT EXISTS Games(
    gameId char(3),
    title char(50),
    genre char(50),
    developer char(50),
    releaseyear int,
    CONSTRAINT games_pk PRIMARY KEY (gameId)
);
--Import games
COPY Games(gameId, title, genre, developer, releaseyear)
FROM '\GameReview\tmp\games.csv'
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
FROM '\GameReview\tmp\Reviews.csv'
DELIMITER ','
CSV HEADER;
