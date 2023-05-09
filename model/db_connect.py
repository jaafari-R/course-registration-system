import mysql.connector

db_con = mysql.connector.connect(
    user='root',
    password='1234',
    host='127.0.0.1',
    database='course_register'
)

db_con.autocommit = True