CREATE DATABASE IF NOT EXISTS cbm_health_db;
USE cbm_health_db;
SHOW TABLES;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Health Metrics Table
CREATE TABLE IF NOT EXISTS health_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    sleep_hours DECIMAL(5,2),
    exercise_minutes INT,
    screen_time DECIMAL(5,2),
    water_intake DECIMAL(5,2),
    caffeine_intake DECIMAL(5,2),
    heart_rate INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Encodings Table
CREATE TABLE IF NOT EXISTS health_encodings (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    encoded_genotypes JSON, 
    encoded_phenotype JSON, 
    model_version INT, -- not sure if we care to track this
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

--- NOTE: WE MIGHT FIND IT BETTER TO COMBINE THE LAST 2 TABLES INTO 1
