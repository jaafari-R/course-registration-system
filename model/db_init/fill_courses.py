import mysql.connector
from courses_data import schedules, courses

def insert_schedule(db_cursor, data):
    try:
        query = ("""
            INSERT INTO courseSchedules
            (id, days, start_time, end_time, room_no)
            VALUES
            (%s, %s, %s, %s, %s)
        """)
        db_cursor.execute(query, data)
    except Exception as e:
        print('Failed to insert schedule')
        print(str(e))

def insert_course(db_cursor, data):
    try:
        query = ("""
            INSERT INTO courses
            (code, name, description, instructor, capacity, schedule)
            VALUES
            (%s, %s, %s, %s, %s, %s)
        """)
        db_cursor.execute(query, data)
    except Exception as e:
        print('Failed to insert Course')
        print(str(e))

def insert_preqrequisite(db_cursor, data):
    try:
        query = ("""
            INSERT INTO coursePrerequisites
            (course, prerequisite_course)
            VALUES
            (%s, %s)
        """)
        db_cursor.execute(query, data)
    except Exception as e:
        print('Failed to insert Course Preqrequisite')
        print(str(e))



def get_course_schedule_id(course_code):
    for schedule in schedules:
        if(schedule[5] == course_code):
            return schedule[0]

def fill_courses():
    db_connection = mysql.connector.connect(
        user='root',
        password='1234',
        host='127.0.0.1',
        database='course_register'
    )

    db_connection.autocommit = True

    db_cursor = db_connection.cursor()

    # insert Schedules into DB
    for schedule in schedules:
        id = schedule[0]
        days = ','.join(schedule[1])
        start_time = schedule[2]
        end_time = schedule[3]
        room = schedule[4]

        data = (id, days, start_time, end_time, room)
        insert_schedule(db_cursor, data)

    # insert Courses into DB
    for course in courses:
        code = course[0]
        name = course[1]
        description = course[2]
        instructor = course[4]
        capacity = course[5]
        schedule_id = get_course_schedule_id(code)

        data = (code, name, description, instructor, capacity, schedule_id)
        insert_course(db_cursor, data)

    # insert Prerequisites
    for course in courses:
        course_code = course[0]
        prerequisite_courses = course[3]

        for prerequisite_course in prerequisite_courses:
            data = (course_code, prerequisite_course)
            insert_preqrequisite(db_cursor, data)

    db_cursor.close()
    db_connection.close()