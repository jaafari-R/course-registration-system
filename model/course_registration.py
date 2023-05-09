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
                SELECT student_id
                FROM sessions
                WHERE cookie = %s
            """)
            self.__db_cursor.execute(query, (cookie,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_session_student_id(self, cookie):
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

    def get_all_courses(self):
        try: 
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
            """)
            self.__db_cursor.execute(query)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def search_courses_by_code(self, code):
        try: 
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    code = %s AND
            """)
            data = (code,)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def search_courses(self, name, instructor):
        try: 
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    name LIKE %s AND
                    instructor LIKE %s
            """)
            data = ('%'+name+'%', '%'+instructor+'%')
            print(data)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_enrollable_courses(slef, student_id):
        try:
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    NOT (
                        SELECT COUNT(*)
                        FROM coursePrerequisites
                        WHERE 
                            NOT EXISTS (
                                SELECT course_code
                                FROM studentsReg
                                WHERE
                                    studentsReg.student_id = %s AND
                                    studentsReg.course_code = courses.code AND
                                    status = 'passed'
                            )
                    ) AND
                    code NOT IN (
                        SELECT course_code
                        FROM studentsReg
                        WHERE
                            student_id = %s AND
                            (
                                status = 'passed' OR
                                status = 'enrolled'
                            )
                    )
            """)
            data = (student_id,)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_enrollable_courses_by_code(self, student_id, code):
        try:
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    code = %s
                    NOT (
                        SELECT COUNT(*)
                        FROM coursePrerequisites
                        WHERE 
                            NOT EXISTS (
                                SELECT course_code
                                FROM studentsReg
                                WHERE
                                    studentsReg.student_id = %s AND
                                    studentsReg.course_code = courses.code AND
                                    status = 'passed'
                            )
                    ) AND
                    code NOT IN (
                        SELECT course_code
                        FROM studentsReg
                        WHERE
                            student_id = %s AND
                            (
                                status = 'passed' OR
                                status = 'enrolled'
                            )
                    )
            """)
            data = (student_id, code)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def search_enrollable_courses(self, name, instructor):
        try:
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    name LIKE %s AND
                    instructor LIKE %s AND
                    NOT (
                        SELECT COUNT(*)
                        FROM coursePrerequisites
                        WHERE 
                            NOT EXISTS (
                                SELECT course_code
                                FROM studentsReg
                                WHERE
                                    studentsReg.student_id = %s AND
                                    studentsReg.course_code = courses.code AND
                                    status = 'passed'
                            )
                    ) AND
                    code NOT IN (
                        SELECT course_code
                        FROM studentsReg
                        WHERE
                            student_id = %s AND
                            (
                                status = 'passed' OR
                                status = 'enrolled'
                            )
                    )
            """)
            data = (student_id, code)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()