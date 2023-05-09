import mysql.connector
from init_tables import init_tables
from fill_courses import fill_courses

db_connection = mysql.connector.connect(
    user='root',
    password='1234',
    host='127.0.0.1',
)

db_connection.autocommit = True
db_cursor = db_connection.cursor()

# -- Create DB --
try:
    db_cursor.execute("CREATE DATABASE course_register")
except Exception as e:
    print("Failed to create DB")
    print(str(e), "\n")

# -- Create Tables --
init_tables()

# -- fill courses and schedules --
fill_courses()

db_cursor.close()
db_connection.close()


