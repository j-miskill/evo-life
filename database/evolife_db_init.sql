-- TODO: Refine Features and types
-- TODO: Preprocess Data 
-- TODO: Connect encodings table to model

CREATE DATABASE IF NOT EXISTS cbm_health_db; -- should have been created by docker-compose
USE cbm_health_db; 
SHOW TABLES;
SET GLOBAL local_infile = 1;


-- USERS TABLE

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(30) PRIMARY KEY,
    breq_amotivation FLOAT,
    breq_external_regulation FLOAT,
    breq_introjected_regulation FLOAT,
    breq_identified_regulation FLOAT,
    breq_intrinsic_regulation FLOAT,
    breq_self_determination VARCHAR(50),
    positive_affect_score FLOAT,
    negative_affect_score FLOAT,
    agreeableness FLOAT,
    conscientiousness FLOAT,
    stability FLOAT,
    intellect FLOAT,
    stai_stress FLOAT,
    stai_stress_category VARCHAR(50),
    ttm_consciousness_raising FLOAT,
    ttm_dramatic_relief FLOAT,
    ttm_environmental_reevaluation FLOAT,
    ttm_self_reevaluation FLOAT,
    ttm_social_liberation FLOAT,
    ttm_counterconditioning FLOAT,
    ttm_helping_relationships FLOAT,
    ttm_reinforcement_management FLOAT,
    ttm_self_liberation FLOAT,
    ttm_stimulus_control FLOAT
) ENGINE=InnoDB;

-- load initial Kaggle individual data into our users table

CREATE TEMPORARY TABLE temp_users (
    user_id VARCHAR(30) PRIMARY KEY,
    breq_amotivation FLOAT,
    breq_external_regulation FLOAT,
    breq_introjected_regulation FLOAT,
    breq_identified_regulation FLOAT,
    breq_intrinsic_regulation FLOAT,
    breq_self_determination VARCHAR(50),
    positive_affect_score FLOAT,
    negative_affect_score FLOAT,
    agreeableness FLOAT,
    conscientiousness FLOAT,
    stability FLOAT,
    intellect FLOAT,
    stai_stress FLOAT,
    stai_stress_category VARCHAR(50),
    ttm_consciousness_raising FLOAT,
    ttm_dramatic_relief FLOAT,
    ttm_environmental_reevaluation FLOAT,
    ttm_self_reevaluation FLOAT,
    ttm_social_liberation FLOAT,
    ttm_counterconditioning FLOAT,
    ttm_helping_relationships FLOAT,
    ttm_reinforcement_management FLOAT,
    ttm_self_liberation FLOAT,
    ttm_stimulus_control FLOAT
);

LOAD DATA INFILE '/var/lib/mysql-files/database_individuals.csv'
INTO TABLE temp_users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    @dummy,
    user_id, 
    breq_amotivation,
    breq_external_regulation,
    breq_introjected_regulation,
    breq_identified_regulation,
    breq_intrinsic_regulation,
    breq_self_determination,
    positive_affect_score,
    negative_affect_score,
    agreeableness,
    conscientiousness,
    stability,
    intellect,
    stai_stress,
    stai_stress_category,
    ttm_consciousness_raising,
    ttm_dramatic_relief,
    ttm_environmental_reevaluation,
    ttm_self_reevaluation,
    ttm_social_liberation,
    ttm_counterconditioning,
    ttm_helping_relationships,
    ttm_reinforcement_management,
    ttm_self_liberation,
    ttm_stimulus_control
);

INSERT IGNORE INTO users (
    user_id, 
    breq_amotivation,
    breq_external_regulation,
    breq_introjected_regulation,
    breq_identified_regulation,
    breq_intrinsic_regulation,
    breq_self_determination,
    positive_affect_score,
    negative_affect_score,
    agreeableness,
    conscientiousness,
    stability,
    intellect,
    stai_stress,
    stai_stress_category,
    ttm_consciousness_raising,
    ttm_dramatic_relief,
    ttm_environmental_reevaluation,
    ttm_self_reevaluation,
    ttm_social_liberation,
    ttm_counterconditioning,
    ttm_helping_relationships,
    ttm_reinforcement_management,
    ttm_self_liberation,
    ttm_stimulus_control
)
SELECT user_id, 
    breq_amotivation,
    breq_external_regulation,
    breq_introjected_regulation,
    breq_identified_regulation,
    breq_intrinsic_regulation,
    breq_self_determination,
    positive_affect_score,
    negative_affect_score,
    agreeableness,
    conscientiousness,
    stability,
    intellect,
    stai_stress,
    stai_stress_category,
    ttm_consciousness_raising,
    ttm_dramatic_relief,
    ttm_environmental_reevaluation,
    ttm_self_reevaluation,
    ttm_social_liberation,
    ttm_counterconditioning,
    ttm_helping_relationships,
    ttm_reinforcement_management,
    ttm_self_liberation,
    ttm_stimulus_control
FROM temp_users;

-- END USERS TABLE

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
    pred_tired BOOLEAN DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;


-- load initial Kaggle daily Data into our users table

CREATE TEMPORARY TABLE temp_health_metrics (
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
);

LOAD DATA INFILE '/var/lib/mysql-files/database_daily.csv'
INTO TABLE temp_health_metrics
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

INSERT IGNORE INTO health_metrics (
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
)
SELECT metric_id,
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
FROM temp_health_metrics;


-- END HEALTH METRICTS TABLE


-- ENCODINGS TABLE

CREATE TABLE IF NOT EXISTS encoded_health_metrics (
    encoding_id VARCHAR(10) PRIMARY KEY,
    metric_id INT,
    user_id VARCHAR(30),
    date DATE NOT NULL,
    day INT,

    encoded_gender FLOAT,
    encoded_nremhr FLOAT,
    encoded_rmssd FLOAT,
    encoded_spo2 FLOAT,
    encoded_exertion_points_percentage FLOAT,
    encoded_responsiveness_points_percentage FLOAT,
    encoded_distance FLOAT,
    encoded_activityType FLOAT,
    encoded_bpm FLOAT,
    encoded_lightly_active_minutes FLOAT,
    encoded_moderately_active_minutes FLOAT,
    encoded_very_active_minutes FLOAT,
    encoded_sedentary_minutes FLOAT,
    encoded_mindfulness_session FLOAT,
    encoded_sleep_duration FLOAT,
    encoded_minutesAsleep FLOAT,
    encoded_minutesAwake FLOAT,
    encoded_sleep_efficiency FLOAT,
    encoded_bmi FLOAT,
    encoded_gym FLOAT,
    encoded_home FLOAT,
    encoded_outdoors FLOAT,

    encoded_stress_score FLOAT,
    encoded_sleep_points_percentage FLOAT,
    encoded_tense_anxious FLOAT,
    encoded_tired FLOAT,

    phenotype FLOAT,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (metric_id) REFERENCES health_metrics(metric_id)
) ENGINE=InnoDB;


-- Inserting Example Data so that I can have something to use for the UI
-- I picked a random user from our daily.csv data

INSERT INTO encoded_health_metrics (
    encoding_id, metric_id, user_id, date, day,
    encoded_gender, encoded_nremhr, encoded_rmssd, encoded_spo2, 
    encoded_exertion_points_percentage, encoded_responsiveness_points_percentage, 
    encoded_distance, encoded_activityType, encoded_bpm, encoded_lightly_active_minutes, 
    encoded_moderately_active_minutes, encoded_very_active_minutes, encoded_sedentary_minutes, 
    encoded_mindfulness_session, encoded_sleep_duration, encoded_minutesAsleep, 
    encoded_minutesAwake, encoded_sleep_efficiency, encoded_bmi, 
    encoded_gym, encoded_home, encoded_outdoors, 
    encoded_stress_score, encoded_sleep_points_percentage, 
    encoded_tense_anxious, encoded_tired, phenotype
) VALUES
('E6368', 6368, '621e2e8e67b776a24055b564', '2021-05-24', 1,
    1.0, 67.2, 39.8, 95.0, 
    78.3, 65.7, 45.1, 5.0, 2.0, 
    72.5, 42.0, 28.5, 15.2, 12.3, 0.0, 
    7.5, 445.3, 90.1, 85.5, 
    24.2, 0.0, 1.0, 0.45, 5.2, 12.3, 0.0, 
    7.5),

('E6369', 6369, '621e2e8e67b776a24055b564', '2021-05-25', 2,
    1.0, 68.0, 41.2, 96.3, 
    80.1, 67.4, 46.2, 4.8, 3.0, 
    73.0, 40.5, 29.0, 14.5, 13.5, 1.0, 
    7.8, 450.2, 89.3, 84.7, 5.2, 12.3, 0.0, 
    7.5, 24.4, 0.0, 1.0, 0.88),

('E6370', 6370, '621e2e8e67b776a24055b564', '2021-05-26', 3,
    1.0, 69.5, 42.3, 96.0, 
    75.5, 64.5, 44.9, 6.0, 2.0, 
    70.3, 43.1, 30.1, 16.0, 14.0, 0.0, 
    7.2, 455.1, 91.2, 87.1, 
    24.0, 1.0, 0.0, 5.2, 12.3, 0.0, 
    7.5, 0.76),

('E6371', 6371, '621e2e8e67b776a24055b564', '2021-05-27', 4,
    1.0, 68.3, 40.0, 95.5, 
    77.0, 63.9, 43.5, 5.2, 2.5, 5.2, 12.3, 0.0, 
    7.5, 74.0, 41.0, 29.8, 15.4, 12.9, 0.0, 
    7.4, 459.6, 90.4, 86.0, 
    24.3, 0.0, 1.0, 0.35),

('E6372', 6372, '621e2e8e67b776a24055b564', '2021-05-28', 5,
    1.0, 67.7, 39.6, 94.8, 
    79.0, 66.0, 47.0, 5.3, 1.5, 
    71.5, 44.0, 30.0, 16.2, 13.7, 1.0, 
    7.6, 463.0, 88.5, 85.0, 5.2, 12.3, 0.0, 
    7.5, 24.6, 1.0, 0.0, 0.95),

('E6373', 6373, '621e2e8e67b776a24055b564', '2021-05-29', 6,
    1.0, 70.2, 43.1, 97.1, 
    76.3, 65.1, 45.5, 6.1, 3.5, 
    69.2, 40.8, 31.0, 15.6, 13.2, 0.0, 
    7.7, 468.3, 92.0, 88.2, 5.2, 12.3, 0.0, 
    7.5, 24.7, 0.0, 1.0, 0.18),

('E6374', 6374, '621e2e8e67b776a24055b564', '2021-05-30', 7,
    1.0, 68.1, 40.5, 95.4, 
    74.0, 62.8, 42.3, 5.9, 2.8, 
    71.8, 41.5, 30.5, 14.8, 12.7, 1.0, 
    7.3, 472.5, 89.0, 84.5, 5.2, 12.3, 0.0, 
    7.5, 24.1, 0.0, 1.0, 0.7),

('E6375', 6375, '621e2e8e67b776a24055b564', '2021-05-31', 8,
    1.0, 69.0, 41.0, 96.5, 
    78.2, 64.3, 46.0, 5.4, 3.2, 
    72.6, 42.0, 30.3, 16.4, 13.1, 1.0, 
    7.9, 478.2, 90.5, 85.2, 5.2, 12.3, 0.0, 
    7.5, 24.8, 1.0, 0.0, 0.8);



-- END ENCODINGS TABLE
