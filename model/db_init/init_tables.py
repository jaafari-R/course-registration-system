import mysql.connector

def init_tables():
    # Connect to DB
    db_connection = mysql.connector.connect(
        user='root',
        password='1234',
        host='127.0.0.1',
        database='course_register'
    )

    db_connection.autocommit = True
    db_cursor = db_connection.cursor()
    

    # -- Create Course-Schedules Table --
    try:
        db_cursor.execute("""
            CREATE TABLE courseSchedules(
                id INT PRIMARY KEY,
                days SET('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                room_no VARCHAR(10) NOT NULL
            )
        """)
    except Exception as e:
        print("Failed to create Course-Schedules table")
        print(str(e), "\n")


    # -- Create Courses Table --
    try:
        db_cursor.execute("""
            CREATE TABLE courses(
                code INT PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                description VARCHAR(512),
                instructor VARCHAR(40) NOT NULL,
                capacity INT NOT NULL,
                schedule INT NOT NULL,
                available BOOLEAN DEFAULT true,
                FOREIGN KEY (schedule) REFERENCES courseSchedules(id)
            );
        """)

    except Exception as e:
        print("Failed to create Courses table")
        print(str(e), "\n")


    # -- Create Course-Prerequisites Table --
    try:
        db_cursor.execute("""
            CREATE TABLE coursePrerequisites(
                course INT,
                prerequisite_course INT,
                FOREIGN KEY (course) REFERENCES courses(code),
                FOREIGN KEY (prerequisite_course) REFERENCES courses(code),
                PRIMARY KEY(course, prerequisite_course)
            );
        """)
    except Exception as e:
        print("Failed to create Course-Prerequisites table")
        print(str(e), "\n")


    # -- Create Students Table --
    try:
        db_cursor.execute("""
            CREATE TABLE students(
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(15) NOT NULL,
                last_name VARCHAR(15) NOT NULL,
                email VARCHAR(30) NOT NULL,
                password VARCHAR(60) NOT NULL,
                viewed_notifications BOOLEAN DEFAULT true,
                admin BOOLEAN
            );
        """)
    except Exception as e:
        print("Failed to create Students table")
        print(str(e), "\n")


    # -- Create Student-Registration Table --
    try:
        db_cursor.execute("""
            CREATE TABLE studentsReg(
                id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT NOT NULL,
                course_code INT NOT NULL,
                status ENUM('passed', 'failed', 'enrolled') NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_code) REFERENCES courses(code)
            )
        """)
    except Exception as e:
        print("Failed to create Student-Registration table")
        print(str(e), "\n")


    # -- Create Notifications Table --
    try:
        db_cursor.execute("""
            CREATE TABLE notifications(
                id INT PRIMARY KEY,
                message VARCHAR(100) NOT NULL
            )
        """)
    except Exception as e:
        print("Failed to create Notifications table")
        print(str(e), "\n")


    # -- Create Sessions Table --
    try:
        db_cursor.execute("""
            CREATE TABLE sessions(
                cookie VARCHAR(32) PRIMARY KEY,
                student_id INT NOT NULL,
                expiration_date DATETIME NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) 
            )
        """)
    except Exception as e:
        print("Failed to create Sessions table")
        print(str(e), "\n")


    db_cursor.close()
    db_connection.close()