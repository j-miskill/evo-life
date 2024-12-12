-- TODO: Refine Features and types
-- TODO: Preprocess Data 
-- TODO: Connect encodings table to model

CREATE DATABASE IF NOT EXISTS cbm_health_db; -- should have been created by docker-compose
USE cbm_health_db; 
SHOW TABLES;
SET GLOBAL local_infile = 1;


-- -- USERS TABLE

-- CREATE TABLE IF NOT EXISTS users (
--     user_id VARCHAR(30) PRIMARY KEY,
--     breq_amotivation FLOAT,
--     breq_external_regulation FLOAT,
--     breq_introjected_regulation FLOAT,
--     breq_identified_regulation FLOAT,
--     breq_intrinsic_regulation FLOAT,
--     breq_self_determination VARCHAR(50),
--     positive_affect_score FLOAT,
--     negative_affect_score FLOAT,
--     agreeableness FLOAT,
--     conscientiousness FLOAT,
--     stability FLOAT,
--     intellect FLOAT,
--     stai_stress FLOAT,
--     stai_stress_category VARCHAR(50),
--     ttm_consciousness_raising FLOAT,
--     ttm_dramatic_relief FLOAT,
--     ttm_environmental_reevaluation FLOAT,
--     ttm_self_reevaluation FLOAT,
--     ttm_social_liberation FLOAT,
--     ttm_counterconditioning FLOAT,
--     ttm_helping_relationships FLOAT,
--     ttm_reinforcement_management FLOAT,
--     ttm_self_liberation FLOAT,
--     ttm_stimulus_control FLOAT
-- ) ENGINE=InnoDB;

-- -- load initial Kaggle individual data into our users table

-- LOAD DATA INFILE '/var/lib/mysql-files/database_individuals.csv'
-- INTO TABLE users
-- FIELDS TERMINATED BY ','
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (
--     @dummy,
--     user_id, 
--     breq_amotivation,
--     breq_external_regulation,
--     breq_introjected_regulation,
--     breq_identified_regulation,
--     breq_intrinsic_regulation,
--     breq_self_determination,
--     positive_affect_score,
--     negative_affect_score,
--     agreeableness,
--     conscientiousness,
--     stability,
--     intellect,
--     stai_stress,
--     stai_stress_category,
--     ttm_consciousness_raising,
--     ttm_dramatic_relief,
--     ttm_environmental_reevaluation,
--     ttm_self_reevaluation,
--     ttm_social_liberation,
--     ttm_counterconditioning,
--     ttm_helping_relationships,
--     ttm_reinforcement_management,
--     ttm_self_liberation,
--     ttm_stimulus_control
-- );

-- -- END USERS TABLE

-- HEALTH METRICTS TABLE

CREATE TABLE IF NOT EXISTS health_metrics (
    metric_id INT PRIMARY KEY,
    user_id VARCHAR(30),
    date DATE NOT NULL,
    nremhr FLOAT,
    rmssd FLOAT,
    spo2 FLOAT,
    stress_score FLOAT,
    sleep_points_percentage FLOAT,
    exertion_points_percentage FLOAT,
    responsiveness_points_percentage FLOAT,
    distance FLOAT,
    activityType VARCHAR(100),
    bpm VARCHAR(50),
    lightly_active_minutes FLOAT,
    moderately_active_minutes FLOAT,
    very_active_minutes FLOAT,
    sedentary_minutes FLOAT,
    mindfulness_session BOOLEAN,
    sleep_duration FLOAT,
    minutesAsleep FLOAT,
    minutesAwake FLOAT,
    sleep_efficiency FLOAT,
    gender VARCHAR(10),
    bmi VARCHAR(10),
    tense_anxious BOOLEAN,
    tired BOOLEAN,
    gym BOOLEAN,
    home BOOLEAN,
    outdoors BOOLEAN,
    day INT,
    pred_bmi VARCHAR(10) DEFAULT NULL,
    pred_tense_anxious BOOLEAN DEFAULT NULL,
    pred_tired BOOLEAN DEFAULT NULL
) ENGINE=InnoDB;


-- load initial Kaggle daily Data into our users table

LOAD DATA INFILE '/var/lib/mysql-files/database_daily.csv'
INTO TABLE health_metrics
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    metric_id,
    user_id,
    date,
    nremhr,
    rmssd,
    spo2,
    stress_score,
    sleep_points_percentage,
    exertion_points_percentage,
    responsiveness_points_percentage,
    distance,
    activityType,
    bpm,
    lightly_active_minutes,
    moderately_active_minutes,
    very_active_minutes,
    sedentary_minutes,
    mindfulness_session,
    sleep_duration,
    minutesAsleep,
    minutesAwake,
    sleep_efficiency,
    gender,
    bmi,
    tense_anxious,
    tired,
    gym,
    home,
    outdoors,
    day
);

-- END HEALTH METRICTS TABLE


-- ENCODINGS TABLE

CREATE TABLE IF NOT EXISTS encoded_health_metrics (
    encoding_id INT PRIMARY KEY,
    user_id VARCHAR(30),
    day INT,
    encoding VARCHAR(75)
) ENGINE=InnoDB;

LOAD DATA INFILE '/var/lib/mysql-files/encodings.csv'
INTO TABLE encoded_health_metrics
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    encoding_id, user_id, day, encoding
);

-- END ENCODINGS TABLE

-- PHENOTYPE TABLE

CREATE TABLE IF NOT EXISTS phenotype_data (
    pheno_id INT PRIMARY KEY,
    user_id VARCHAR(30),
    month INT,
    phenotype_score FLOAT
) ENGINE=InnoDB;

LOAD DATA INFILE '/var/lib/mysql-files/database_phenotype_data.csv'
INTO TABLE phenotype_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    pheno_id, user_id, month, phenotype_score
);

-- END PHENOTYPE TABLE
