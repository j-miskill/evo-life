from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from trigger_pipeline import trigger_inference
from db_connector import get_db_connection
import os

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
    cursor.execute("SELECT * FROM health_metrics")
    health_metrics = cursor.fetchall()
    cursor.execute("SELECT DISTINCT user_id FROM health_metrics")
    users = cursor.fetchall()
    cursor.execute("SELECT DISTINCT date FROM health_metrics")
    metric_dates = cursor.fetchall()
    conn.close()
    return render_template("index.html", health_metrics=health_metrics, users=users, metric_dates=metric_dates)

@app.route("/get_metrics/<user_id>/<metric_date>")
def get_metrics(user_id, metric_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM health_metrics WHERE user_id = %s AND date = %s", (user_id, metric_date))
    health_metrics = cursor.fetchall()
    conn.close()
    return jsonify(health_metrics)


@app.route("/get_encodings/<user_id>/<metric_date>")
def get_encodings(user_id, metric_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM encoded_health_metrics WHERE user_id = %s AND date = %s", (user_id, metric_date))
    health_encodings = cursor.fetchall()
    conn.close()
    return jsonify(health_encodings)

# @app.route("/visualize", methods=["GET"])
# def visualize():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM encoded_health_metrics")
#     data = cursor.fetchall()
#     conn.close()
#     return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)