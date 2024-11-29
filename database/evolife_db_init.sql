-- TODO: Refine Featuures and types
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
    day INT
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
    gender VARCHAR(10),
    date DATE NOT NULL,
    day INT,
    encoded_nremhr FLOAT,
    encoded_rmssd FLOAT,
    encoded_spo2 FLOAT,
    encoded_stress_score FLOAT,
    encoded_sleep_points_percentage FLOAT,
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
    encoded_tense_anxious FLOAT,
    encoded_tired FLOAT,
    encoded_gym FLOAT,
    encoded_home FLOAT,
    encoded_outdoors FLOAT,
    FOREIGN KEY (metric_id) REFERENCES health_metrics(metric_id)
) ENGINE=InnoDB;


-- Inserting Example Data so that I can have something to use for the UI
-- I picked a random user from our daily.csv data

INSERT INTO encoded_health_metrics (
    encoding_id, metric_id, user_id, gender, date, day,
    encoded_nremhr, encoded_rmssd, encoded_spo2, encoded_stress_score, 
    encoded_sleep_points_percentage, encoded_exertion_points_percentage, 
    encoded_responsiveness_points_percentage, encoded_distance, encoded_activityType, 
    encoded_bpm, encoded_lightly_active_minutes, encoded_moderately_active_minutes, 
    encoded_very_active_minutes, encoded_sedentary_minutes, encoded_mindfulness_session, 
    encoded_sleep_duration, encoded_minutesAsleep, encoded_minutesAwake, encoded_sleep_efficiency, 
    encoded_bmi, encoded_tense_anxious, encoded_tired, encoded_gym, encoded_home, encoded_outdoors
) VALUES
('E6368', 6368, '621e362467b776a2404ad513', 'Male', '2021-04-08', 1, 
    67.2, 39.8, 95.0, 21.1, 
    78.3, 65.7, 45.1, 5.0, 2.0, 
    72.5, 42.0, 28.5, 15.2, 12.3, 0.0, 
    7.5, 445.3, 90.1, 85.5, 
    24.2, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6369', 6369, '621e362467b776a2404ad513', 'Male', '2021-04-09', 2, 
    68.0, 41.2, 96.3, 22.4, 
    80.1, 67.4, 46.2, 4.8, 3.0, 
    73.0, 40.5, 29.0, 14.5, 13.5, 1.0, 
    7.8, 450.2, 89.3, 84.7, 
    24.4, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6370', 6370, '621e362467b776a2404ad513', 'Male', '2021-04-10', 3, 
    69.5, 42.3, 96.0, 21.0, 
    75.5, 64.5, 44.9, 6.0, 2.0, 
    70.3, 43.1, 30.1, 16.0, 14.0, 0.0, 
    7.2, 455.1, 91.2, 87.1, 
    24.0, 1.0, 0.0, 1.0, 1.0, 0.0),

('E6371', 6371, '621e362467b776a2404ad513', 'Male', '2021-04-12', 4, 
    68.3, 40.0, 95.5, 20.2, 
    77.0, 63.9, 43.5, 5.2, 2.5, 
    74.0, 41.0, 29.8, 15.4, 12.9, 0.0, 
    7.4, 459.6, 90.4, 86.0, 
    24.3, 0.0, 1.0, 0.0, 0.0, 1.0),

('E6372', 6372, '621e362467b776a2404ad513', 'Male', '2021-04-13', 5, 
    67.7, 39.6, 94.8, 19.9, 
    79.0, 66.0, 47.0, 5.3, 1.5, 
    71.5, 44.0, 30.0, 16.2, 13.7, 1.0, 
    7.6, 463.0, 88.5, 85.0, 
    24.6, 1.0, 0.0, 1.0, 1.0, 0.0),

('E6373', 6373, '621e362467b776a2404ad513', 'Male', '2021-04-16', 6, 
    70.2, 43.1, 97.1, 18.5, 
    76.3, 65.1, 45.5, 6.1, 3.5, 
    69.2, 40.8, 31.0, 15.6, 13.2, 0.0, 
    7.7, 468.3, 92.0, 88.2, 
    24.7, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6374', 6374, '621e362467b776a2404ad513', 'Male', '2021-04-17', 7, 
    68.1, 40.5, 95.4, 19.4, 
    74.0, 62.8, 42.3, 5.9, 2.8, 
    71.8, 41.5, 30.5, 14.8, 12.7, 1.0, 
    7.3, 472.5, 89.0, 84.5, 
    24.1, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6375', 6375, '621e362467b776a2404ad513', 'Male', '2021-04-19', 8, 
    69.0, 41.0, 96.5, 20.8, 
    78.2, 64.3, 46.0, 5.4, 3.2, 
    72.6, 42.0, 30.3, 16.4, 13.1, 1.0, 
    7.9, 478.2, 90.5, 85.2, 
    24.8, 1.0, 0.0, 1.0, 0.0, 0.0),

('E6376', 6376, '621e362467b776a2404ad513', 'Male', '2021-04-20', 9, 
    70.0, 42.0, 97.0, 21.0, 
    75.3, 64.0, 44.0, 6.5, 2.3, 
    70.8, 43.2, 30.7, 15.1, 14.0, 0.0, 
    7.5, 483.4, 92.3, 87.0, 
    24.5, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6377', 6377, '621e362467b776a2404ad513', 'Male', '2021-04-21', 10, 
    69.5, 41.8, 96.8, 20.3, 
    76.5, 63.2, 45.3, 6.2, 3.0, 
    71.0, 44.1, 30.9, 15.7, 12.5, 1.0, 
    7.8, 488.0, 90.0, 83.5, 
    24.9, 1.0, 0.0, 1.0, 1.0, 0.0),

('E6378', 6378, '621e362467b776a2404ad513', 'Male', '2021-04-22', 11, 
    68.8, 40.7, 95.2, 21.5, 
    77.8, 65.4, 46.3, 6.7, 2.5, 
    73.2, 41.9, 31.1, 15.9, 13.3, 0.0, 
    7.9, 493.7, 91.5, 86.8, 
    25.0, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6379', 6379, '621e362467b776a2404ad513', 'Male', '2021-04-23', 12, 
    67.9, 39.9, 95.6, 19.8, 
    75.9, 64.1, 44.7, 5.8, 3.1, 
    72.4, 42.3, 30.8, 16.3, 14.2, 1.0, 
    7.6, 498.1, 92.5, 87.3, 
    25.1, 1.0, 0.0, 1.0, 0.0, 0.0),

('E6380', 6380, '621e362467b776a2404ad513', 'Male', '2021-04-24', 13, 
    69.3, 41.5, 96.2, 20.1, 
    78.4, 64.7, 45.8, 6.4, 2.9, 
    70.7, 43.6, 31.2, 15.0, 13.9, 0.0, 
    7.7, 503.0, 90.9, 85.9, 
    25.2, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6381', 6381, '621e362467b776a2404ad513', 'Male', '2021-04-25', 14, 
    68.4, 40.2, 95.7, 21.3, 
    77.2, 63.5, 44.2, 6.6, 3.3, 
    71.4, 42.7, 30.6, 16.1, 13.4, 1.0, 
    7.6, 507.8, 91.2, 86.5, 
    25.3, 1.0, 0.0, 1.0, 0.0, 0.0),

('E6382', 6382, '621e362467b776a2404ad513', 'Male', '2021-04-26', 15, 
    70.1, 42.6, 97.2, 20.0, 
    75.8, 64.6, 45.6, 6.9, 2.6, 
    71.9, 43.3, 31.3, 15.8, 13.6, 0.0, 
    7.8, 512.3, 92.0, 87.6, 
    25.4, 0.0, 1.0, 1.0, 0.0, 0.0),

('E6383', 6383, '621e362467b776a2404ad513', 'Male', '2021-04-27', 16, 
    69.4, 41.9, 96.6, 20.7, 
    76.9, 64.2, 46.1, 6.8, 2.7, 
    72.0, 42.9, 30.4, 15.5, 13.8, 1.0, 
    7.5, 517.6, 91.8, 86.3, 
    25.5, 1.0, 0.0, 1.0, 0.0, 0.0);


-- ENCODINGS TABLE
