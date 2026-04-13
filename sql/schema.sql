-- =========================================
-- GamePulse Database Schema
-- PostgreSQL
-- =========================================

-- Drop tables (safe re-run)
DROP TABLE IF EXISTS play_sessions CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS purchases CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS developers CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS platforms CASCADE;

-- =========================================
-- Reference Tables
-- =========================================

CREATE TABLE developers (
    developer_id SERIAL PRIMARY KEY,
    developer_name VARCHAR(100) NOT NULL UNIQUE,
    headquarters VARCHAR(100),
    founded_year INT
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE platforms (
    platform_id SERIAL PRIMARY KEY,
    platform_name VARCHAR(50) NOT NULL UNIQUE
);

-- =========================================
-- Core Entity Tables
-- =========================================

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50),
    join_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE games (
    game_id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    release_date DATE,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    developer_id INT NOT NULL,
    genre_id INT NOT NULL,
    platform_id INT NOT NULL,

    CONSTRAINT fk_games_developer
        FOREIGN KEY (developer_id)
        REFERENCES developers(developer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_games_genre
        FOREIGN KEY (genre_id)
        REFERENCES genres(genre_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_games_platform
        FOREIGN KEY (platform_id)
        REFERENCES platforms(platform_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT uq_game_unique
        UNIQUE (title, platform_id, release_date)
);

-- =========================================
-- Transactions
-- =========================================

CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount_paid DECIMAL(10,2) NOT NULL CHECK (amount_paid >= 0),

    CONSTRAINT fk_purchases_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_purchases_game
        FOREIGN KEY (game_id)
        REFERENCES games(game_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_reviews_game
        FOREIGN KEY (game_id)
        REFERENCES games(game_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_player_game_review
        UNIQUE (player_id, game_id)
);

CREATE TABLE play_sessions (
    session_id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    game_id INT NOT NULL,
    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hours_played DECIMAL(6,2) NOT NULL CHECK (hours_played > 0),

    CONSTRAINT fk_sessions_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_sessions_game
        FOREIGN KEY (game_id)
        REFERENCES games(game_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);