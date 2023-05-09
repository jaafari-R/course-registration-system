from model.db_connect import db_con

class CourseRegisterationModel:
    def __init__(self):
        self.__db_cursor = db_con.cursor()

    def create_student(self, first_name, last_name, email, hashed_password):
        try:
            query = ("""
                INSERT INTO students 
                (first_name, last_name, email, password)
                VALUES
                (%s, %s, %s, %s)
            """)
            data = (first_name, last_name, email, hashed_password)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return False
        return True

    def get_student_id(self, email):
        try:
            query = ("""
                SELECT id
                FROM students
                WHERE email = %s
            """)
            self.__db_cursor.execute(query, (email,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_student_password(self, email):
        try:
            query = ("""
                SELECT password
                FROM students
                WHERE email = %s
            """)
            self.__db_cursor.execute(query, (email,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def create_session(self, student_id, cookie, expiration_date):
        try:
            query = ("""
                INSERT INTO sessions
                (cookie, student_id, expiration_date)
                VALUES
                (%s, %s, %s)
            """)
            data = (cookie, student_id, expiration_date)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return False
        return True

    def get_session_exp_date(self, cookie):
        try:
            query = ("""
                SELECT expiration_date
                FROM sessions
                WHERE cookie = %s
            """)
            self.__db_cursor.execute(query, (cookie,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def delete_session(self, cookie):
        try:
            query = ("""
                DELETE FROM sessions
                WHERE cookie = %s
            """)
            self.__db_cursor.execute(query, (cookie,))
        except Exception as e:
            print(str(e))
            return False
        return True

    # TODO
    def create_course(self):
        pass

    # TODO
    def get_courses(self):
        pass

    # TODO
    def search_courses(self, course_code, course_name, course_instructor):
        pass
