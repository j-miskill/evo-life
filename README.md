# Evo-Life

Evolife is a machine learning-driven health tracking and phenotype prediction platform. This repository integrates an Airflow pipeline, a MySQL database, and a Flask-based web application for seamless data processing and user interaction.

**Course**: Computational Behavior Modeling \
**Project**: Genetically modeling Health Metrics and Lifestyle \
**POCs**: Jackson Miskill, Jett Yan, Tripp Mims, Joseph Okeno-Storms


---
## Repository Structure (In Progress)

```plaintext
/project-root
├── airflow
|   ├── dags/
│   │   ├── inference_pipeline.py   # Phenotype Inference Pipeline/DAG
│   │   └── training_pipeline.py    # Model Training Pipeline/DAG
│   └── airflow.cfg                 # Airflow configuration file. Used for pipeline variables
├── app/                        # Core application folder
│   ├── docker/              
│   │   ├── Dockerfile          # Dockerfile to build the Flask app images
│   │   └── requirements.txt    # Python dependencies for the Flask App
│   ├── logs/                   # App logs
│   ├── static/                 # Static files (CSS, JS, images)
│   │   ├── style.css 
│   ├── templates/           
│   │   ├── index.html       # Main HTML script for app
│   ├── app.py               # Main entry point for the app
│   ├── config.py            # App configuration (database, secrets)
│   └── init_cbm_db.py       # Connecting app with DB
├── database/                # Database initialization and SQL scripts
│   └── evolife_db_init.sql  # MySQL Table schemas for the application
├── models/                  # Folder for pretrained model and related files
│   └── cbm_model.pkl        # Example pkl model file. Final Name TBD
├── prepped/                 # Processed Data
│   ├── daily.csv            # Daily health data 
│   └── individual.csv       # Individual health data
├── src/                     # Main Code repository
│   ├── cbm.py               # Our Python scripts
│   └── cbm.ipynb            # Our Python notebooks
├── docker-compose.yml       # Docker Compose setup for airflow, db, and app services
├── LICENSE                  # License
└── README.md                # Project documentation
```

---

## Tools (In Progress)

- Programming Languages
    - Python
    - HTML
    - JavaScript
    - CSS

- Orchestration
    - Airflow

- Application
    - Flask

- Containerization
    - Docker

---

## Database (In Progress)

**DB Name**: cbm_health_db \
**Tables**:
- **users**: to store user information
- **health_metrics**: to store raw health metrics for each user (decoded health metrics & phentoypes)
- **health_encodings**: to store encoded health metrics (genotypes) and encoded phenotype

---

## Docker Compose Setup

The `docker-compose.yml` file orchestrates the various services required to run the Evolife project.

### Services Overview
1. **Airflow**: Manages workflows and orchestrates the inference pipeline.
2. **MySQL**: Database service for storing user data, health metrics, and inference results.
3. **App**: The user interface (UI) and backend for the application.


### Key Services in `docker-compose.yaml`

1. **Airflow Scheduler**: Responsible for scheduling Airflow DAG runs.
   - **Environment Variables**:
     - `AIRFLOW__CORE__EXECUTOR`: Sets the executor (e.g., CeleryExecutor, LocalExecutor).
     - `AIRFLOW__CORE__SQL_ALCHEMY_CONN`: Defines the connection string for the metadata database.
   - **Volumes**:
     - Mounts DAGs and configuration files.
   - **Ports**: Exposes the Airflow webserver on port `8080`.

2. **PostgreSQL Database (cbm_airflow_pg_db)**: Stores user data and Airflow metadata.
   - **Environment Variables**:
     - `POSTGRES_PASSWORD`: Root password for the database.
     - `POSTGRES_USER`: Root user for the db
     - `POSTGRES_DB`: Default database to create on startup.
   - **Volumes**:
     - Persists database data between container restarts.

3. **Flask App**: Runs the core application.
   - **Environment Variables**:
     - Application-specific environment variables can be defined here (e.g., database connection strings).
   - **Ports**:
     - Port: `5050`.

4. **MySQL Database (cbm_app_db)**
    - **Environment Variables**:
        - `MYSQL_ROOT_PASSWORD`: Root password for the database
        - `MYSQL_PASSWORD`: password for the database.
        - `MYSQL_USER`: Root user for the db
        - `MYSQL_DATABASE`: Default database to create on startup.
    - **Ports**:
        - Port: `3306`


### Volumes

#### Docker Volumes
Docker volumes are used to persist data and ensure that critical information remains available even if the containers are stopped or recreated. 

- `mysql_data`
    - Stores the data for the MySQL database, including tables, user data, health metrics, and inference results
    - Ensures that database information is not lost when the MySQL container is restarted or removed

- `airflow_postgres_data`
    - Stores metadata for Airflow, including DAG execution states, task history, and schedules
    - Allows Airflow to maintain its state (e.g., completed tasks, active workflows) even after container restarts

- `airflow_data`
    - Stores configuration files, logs, and other runtime data generated by Airflow during DAG execution
    - Helps retain logs and other critical files needed for debugging or auditing workflow runs


#### Airflow Volumes 
The docker-compose.yml file uses volumes to persist data and share files between the host and containers:
- `./airflow/dags:/opt/airflow/dags`: Mounts DAG definitions to the Airflow container
- `./database:/docker-entrypoint-initdb.d`: Mounts SQL scripts for database initialization
- `./app:/app`: Mounts the app source code for development


---
### Helpful Commands
Run these commands from our project root:

1. **Start all Docker services**:
    ```bash
    docker-compose -f docker-compose.yaml up -d
    ```
    Starts all containers in detached mode.

2. **Stop all Docker services**:
    ```bash
    docker-compose down
    ```
    Stops and removes all containers, networks, and volumes.

3. **View Docker logs**:
    ```bash
    docker-compose logs -f [service_name]
    ```
    Example: `docker-compose logs -f app`

4. **Rebuild Docker images** (if Dockerfile changes):
    ```bash
    docker-compose -f docker-compose.yaml up -d --build
    ```

5. More Commands Coming Soon



---

### Ports

- Airflow Webserver: http://localhost:8080
    - Useful for viewing Training and Inference Pipelines and manually running them
- App: http://localhost:5050
- MySQL: `3306`
    - If we need direct access from tools like MySQL Workbench


