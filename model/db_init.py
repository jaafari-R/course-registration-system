import mysql.connector

db_connection = mysql.connector.connect(
    user='root',
    password='1234',
    host='127.0.0.1',
)

db_cursor = db_connection.cursor()

try:
    db_cursor.execute("CREATE DATABASE course_register")
except:
    pass 

# -- Show Databases --
# db_cursor.execute("SHOW DATABASES")
# for db in db_cursor:
#     print(db[0])

db_connection.close()