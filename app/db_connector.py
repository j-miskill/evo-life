import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
    host=os.getenv("DB_HOST", "cbm-mysql-db"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "cbmteam"),
    password=os.getenv("DB_PASSWORD", "evolife"),
    database=os.getenv("DB_NAME", "cbm_health_db")
)

