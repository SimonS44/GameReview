DROP TABLE Games; --remove / outcomment if first time running code.

CREATE TABLE IF NOT EXISTS Games(
    id char(4),
    title char(50),
    genre char(50),
    developerid char(50),
    releaseyear int,
    CONSTRAINT games_pk PRIMARY KEY (id)
);

COPY Games(id, title, genre, developerid, releaseyear)
FROM 'C:\Users\simon\Desktop\DIS\GameReview\GameReview\tmp\games.csv'
DELIMITER ','
CSV HEADER;