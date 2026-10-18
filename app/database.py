import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        port="3307",
        user="root",
        password="Sum10_slam",
        database="vehicle_parking"
    )
    return db