import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Asth@123",
    database="school"
)

if connection.is_connected():
    print("Database Connected Successfully")