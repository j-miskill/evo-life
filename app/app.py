from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
# from trigger_pipeline import trigger_inference
from db_connector import get_db_connection
import os
import pandas as pd
import calendar

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "database")

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT user_id FROM phenotype_data")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM health_metrics WHERE user_id IN (SELECT DISTINCT user_id FROM phenotype_data)")
    health_metrics = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT month(date) AS month FROM health_metrics WHERE user_id IN (SELECT DISTINCT user_id FROM phenotype_data)")
    months = cursor.fetchall()
    
    conn.close()
    return render_template("index.html", health_metrics=health_metrics, users=users, months=months)

@app.route("/get_metrics/<user_id>/<month>")
def get_metrics(user_id, month):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM health_metrics WHERE user_id = %s AND month(date) = %s", (user_id, month))
    health_metrics = cursor.fetchall()
    conn.close()
    return jsonify(health_metrics)

@app.route("/get_encodings/<user_id>/<month>")
def get_encodings(user_id, month):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT *, REPLACE(REPLACE(encoding,'[',''),']','') as encoding_stripped FROM encoded_health_metrics WHERE (user_id = %s AND day IN (SELECT day FROM health_metrics WHERE month(date) = %s))", (user_id, month))
    health_encodings = cursor.fetchall()
    conn.close()
    health_encodings = pd.DataFrame(health_encodings)
    health_encodings['encoding_sum'] = health_encodings['encoding_stripped'].apply(lambda cell: sum(map(int, cell.split())))
    health_encodings_dict = health_encodings.to_dict(orient='records')

    return jsonify(health_encodings_dict)

@app.route("/get_phenotypes/<user_id>/<month>")
def get_phenotype(user_id, month):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    print("GETTING MONTH NAME HERE......")
    print(month)
    print(calendar.month_name[int(month)])
    cursor.execute("SELECT phenotype_score FROM phenotype_data WHERE (user_id = %s AND month = %s)", (user_id, calendar.month_name[int(month)]))
    phenotype_score = cursor.fetchone()
    conn.close()
    return jsonify([phenotype_score] if phenotype_score else [])

@app.route("/get_metric_trends/<user_id>")
def get_metric_trends(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch data for the last three months
    query = """
        SELECT * 
        FROM health_metrics 
        WHERE user_id = %s
            AND date >= DATE_SUB((SELECT MAX(date) FROM health_metrics 
                                WHERE user_id = %s), INTERVAL 2 MONTH)
        ORDER BY date ASC;

    """
    cursor.execute(query, (user_id, user_id))
    health_metric_trends = cursor.fetchall()
    conn.close()
    
    return jsonify(health_metric_trends)

@app.route("/get_phenotype_trends/<user_id>")
def get_phenotype_trends(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch data for the last three months
    query = """
        SELECT month, phenotype_score FROM (
            SELECT * FROM phenotype_data ph
            WHERE ph.user_id = %s
            ORDER BY ph.month DESC
            LIMIT 12
        ) nph
        ORDER BY nph.month ASC;

    """
    cursor.execute(query, (user_id,))
    phenotype_trends = cursor.fetchall()
    conn.close()
    
    return jsonify(phenotype_trends)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)