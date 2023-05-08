import mysql.connector

db_connection = mysql.connector.connect(
    user='root',
    password='1234',
    host='127.0.0.1',
    database='course_register'
)
