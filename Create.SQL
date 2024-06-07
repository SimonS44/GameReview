DROP TABLE Games; --remove / outcomment if first time running code.

CREATE TABLE IF NOT EXISTS Games(
    id char(4),
    title char(50),
    genre char(50),
    developer char(50),
    releaseyear int,
    CONSTRAINT games_pk PRIMARY KEY (id)
);

COPY Games(id, title, genre, developer, releaseyear)
FROM 'YOUR_PATH\GameReview\GameReview\tmp\games.csv'
DELIMITER ','
CSV HEADER;

--Users
CREATE TABLE IF NOT EXISTS users(
    username char(20) NOT NULL,
    password char(20) NOT NULL,
    mail char(20) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username)
);