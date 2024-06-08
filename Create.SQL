DROP TABLE Games CASCADE; 	--remove / outcomment if first time running code.
DROP TABLE users; 	--remove / outcomment if first time running code.
DROP TABLE reviews;	--remove / outcomment if first time running code.
DROP TABLE Platforms CASCADE;     --remove / outcomment if first time running code.;
DROP TABLE GamePlatforms; --remove / outcomment if first time running code.;

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
FROM 'C:\Users\simon\Desktop\DIS\GameReview\GameReview\tmp\games.csv'
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
FROM 'C:\Users\simon\Desktop\DIS\GameReview\GameReview\tmp\Reviews.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS Platforms(
   platform_id SERIAL PRIMARY KEY,
   platform_name VARCHAR(50) NOT NULL UNIQUE
);

COPY Platforms(platform_id, platform_name)
FROM 'C:\Users\simon\Desktop\DIS\GameReview\GameReview\tmp\Platforms.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS GamePlatforms(
   gameId CHAR(3) NOT NULL,
   platform_id INT NOT NULL,
   CONSTRAINT fk_game FOREIGN KEY (gameId) REFERENCES Games(gameId) ON DELETE CASCADE,
   CONSTRAINT fk_platform FOREIGN KEY (platform_id) REFERENCES Platforms(platform_id) ON DELETE CASCADE,
   CONSTRAINT pk_game_platform PRIMARY KEY (gameId, platform_id)
);

COPY GamePlatforms(gameId, platform_id)
FROM 'C:\Users\simon\Desktop\DIS\GameReview\GameReview\tmp\GamePlatforms.csv'
DELIMITER ','
CSV HEADER;