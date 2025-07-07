-- SQL Scripts for Table Generation and Initial Data

-- Table for User
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Table for Place
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Table for Review
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5) NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    UNIQUE (user_id, place_id)
);

-- Table for Amenity
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- Associative table for place_amenity
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert data for admin user
INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$wHTbB2lfTqqVZbEN/1Jgfe9zqgsv0rUZr58AeC8/rYcHJhQ7nMLcC',
    TRUE
);

-- Insert data for amenity
INSERT INTO amenities (id, name)
VALUES 
    (UUID(), 'WiFi'),
    (UUID(), 'Swimming Pool'),
    (UUID(), 'Air Conditioning');


-- TESTS
-- View users
SELECT * FROM users;

-- Check that the tables exist
SHOW TABLES;

-- Check that the admin user is correctly inserted
SELECT * FROM users WHERE email = 'admin@hbnb.io';

-- Check that the is_admin field is TRUE
SELECT email, is_admin FROM users WHERE email = 'admin@hbnb.io';

-- Check that the equipment is present
SELECT * FROM amenities;


-- CRUD for users
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('user-001', 'Alice', 'Test', 'alice@test.io', 'hashedpw', FALSE);

SELECT * FROM users WHERE email = 'alice@test.io';

-- Updates the first name
UPDATE users SET first_name = 'Alicia' WHERE email = 'alice@test.io';

-- Deletes the user
DELETE FROM users WHERE email = 'alice@test.io';


-- CRUD for places
INSERT INTO places (
    id, title, description, price, latitude, longitude, owner_id
) VALUES (
    'place-001',
    'Appartement Paris Centre',
    'Bel appartement rénové',
    120.00,
    48.8566,
    2.3522,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- View places
SELECT * FROM places;

-- Read specific place
SELECT * FROM places WHERE id = 'place-001';

-- Update price
UPDATE places SET price = 135.00 WHERE id = 'place-001';

-- Delete place
DELETE FROM places WHERE id = 'place-001';


-- CRUD for reviews
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES ('review-001', 'Très bon séjour', 5, 'user-001', 'place-001');

-- Read review
SELECT * FROM reviews WHERE user_id = 'user-001';

-- Update review
UPDATE reviews SET rating = 4, text = 'Séjour agréable' WHERE id = 'review-001';

-- Delete review
DELETE FROM reviews WHERE id = 'review-001';


-- CRUD for amenities
INSERT INTO amenities (id, name) VALUES ('amenity-999', 'Jacuzzi');

-- Read amenity
SELECT * FROM amenities WHERE id = 'amenity-999';

-- Update amenity
UPDATE amenities SET name = 'Jacuzzi extérieur' WHERE id = 'amenity-999';

-- Delete amenity
DELETE FROM amenities WHERE id = 'amenity-999';


-- READ and DELETE for place_amenity
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('place-001', 'amenity-999');

SELECT * FROM place_amenity WHERE place_id = 'place-001';

DELETE FROM place_amenity WHERE place_id = 'place-001' AND amenity_id = 'amenity-999';