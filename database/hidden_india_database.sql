-- ============================================
-- HIDDEN INDIA DATABASE
-- DATABASE SCHEMA
-- ============================================

CREATE DATABASE IF NOT EXISTS hidden_india;

USE hidden_india;


-- ============================================
-- 1. MAIN DESTINATION TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS destinations (
    id VARCHAR(50) PRIMARY KEY,
    slug VARCHAR(150) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    state VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    tagline TEXT,
    overview TEXT,
    why_visit TEXT,
    type VARCHAR(100),
    budget INT,
    budget_label VARCHAR(50),
    duration_days INT,
    best_season VARCHAR(100),
    difficulty VARCHAR(50),
    crowd VARCHAR(50),
    alternative_to VARCHAR(150),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6)
);


-- ============================================
-- 2. STYLES
-- ============================================

CREATE TABLE IF NOT EXISTS styles (
    style_id INT AUTO_INCREMENT PRIMARY KEY,
    style_name VARCHAR(100) UNIQUE NOT NULL
);


-- ============================================
-- 3. DESTINATION-STYLES RELATIONSHIP
-- ============================================

CREATE TABLE IF NOT EXISTS destination_styles (
    destination_id VARCHAR(50),
    style_id INT,

    PRIMARY KEY (destination_id, style_id),

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE,

    FOREIGN KEY (style_id)
        REFERENCES styles(style_id)
        ON DELETE CASCADE
);


-- ============================================
-- 4. SEASONS
-- ============================================

CREATE TABLE IF NOT EXISTS seasons (
    season_id INT AUTO_INCREMENT PRIMARY KEY,
    season_name VARCHAR(50) UNIQUE NOT NULL
);


-- ============================================
-- 5. DESTINATION-SEASONS RELATIONSHIP
-- ============================================

CREATE TABLE IF NOT EXISTS destination_seasons (
    destination_id VARCHAR(50),
    season_id INT,

    PRIMARY KEY (destination_id, season_id),

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE,

    FOREIGN KEY (season_id)
        REFERENCES seasons(season_id)
        ON DELETE CASCADE
);


-- ============================================
-- 6. ACTIVITIES
-- ============================================

CREATE TABLE IF NOT EXISTS activities (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_name VARCHAR(255) UNIQUE NOT NULL
);


-- ============================================
-- 7. DESTINATION-ACTIVITIES RELATIONSHIP
-- ============================================

CREATE TABLE IF NOT EXISTS destination_activities (
    destination_id VARCHAR(50),
    activity_id INT,

    PRIMARY KEY (destination_id, activity_id),

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE,

    FOREIGN KEY (activity_id)
        REFERENCES activities(activity_id)
        ON DELETE CASCADE
);


-- ============================================
-- 8. FOODS
-- ============================================

CREATE TABLE IF NOT EXISTS foods (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id VARCHAR(50),
    food_name VARCHAR(255) NOT NULL,

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- ============================================
-- 9. CAFES
-- ============================================

CREATE TABLE IF NOT EXISTS cafes (
    cafe_id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id VARCHAR(50),
    cafe_name VARCHAR(255) NOT NULL,

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- ============================================
-- 10. DESTINATION IMAGES
-- ============================================

CREATE TABLE IF NOT EXISTS destination_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id VARCHAR(50),
    image_url TEXT NOT NULL,
    image_type VARCHAR(30),

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- ============================================
-- 11. PHOTO SPOTS
-- ============================================

CREATE TABLE IF NOT EXISTS photo_spots (
    photo_spot_id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id VARCHAR(50),
    spot_name TEXT NOT NULL,

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- ============================================
-- 12. NEARBY DESTINATIONS
-- Used when a nearby place is also one of
-- the Hidden India destinations.
-- ============================================

CREATE TABLE IF NOT EXISTS nearby_destinations (
    destination_id VARCHAR(50),
    nearby_destination_id VARCHAR(50),

    PRIMARY KEY (destination_id, nearby_destination_id),

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE,

    FOREIGN KEY (nearby_destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- ============================================
-- 13. NEARBY PLACES
-- General nearby attractions, cities,
-- villages, landmarks, etc.
-- ============================================

CREATE TABLE IF NOT EXISTS nearby_places (
    nearby_place_id INT AUTO_INCREMENT PRIMARY KEY,
    destination_id VARCHAR(50) NOT NULL,
    place_name VARCHAR(255) NOT NULL,

    FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE CASCADE
);


-- ============================================
-- END OF HIDDEN INDIA DATABASE SCHEMA
-- ============================================
