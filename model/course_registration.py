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

    def get_session_student_id(self, cookie):
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

    def search_courses(self, code, name, instructor):
        try: 
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    CAST(code AS CHAR) LIKE %s AND
                    name LIKE %s AND
                    instructor LIKE %s
            """)
            data = ('%'+code+'%', '%'+name+'%', '%'+instructor+'%')
            print(data)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_enrollable_courses(self, student_id):
        try:
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    available = True AND
                    NOT (
                        SELECT COUNT(*)
                            FROM coursePrerequisites
                            WHERE 
                                coursePrerequisites.course = courses.code AND 
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
            data = (student_id, student_id)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def search_enrollable_courses(self, student_id, code, name, instructor):
        try:
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE
                    available = True AND
                    CAST(code AS CHAR) LIKE %s AND
                    name LIKE %s AND
                    instructor LIKE %s AND
                    NOT (
                        SELECT COUNT(*)
                            FROM coursePrerequisites
                            WHERE 
                                coursePrerequisites.course = courses.code AND 
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
            data = ('%'+code+'%', '%'+name+'%', '%'+instructor+'%', student_id, student_id)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_course(self, code):
        try:
            query = ("""
                SELECT *
                FROM courses
                WHERE code = %s
            """)
            self.__db_cursor.execute(query, (code,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_course_prerequisites(self, code):
        try:
            query = ("""
                SELECT prerequisite_course
                FROM coursePrerequisites
                WHERE course = %s
            """)
            self.__db_cursor.execute(query, (code,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_registered_courses(self, student_id):
        try:
            query = ("""
                SELECT name, code, instructor, capacity
                FROM courses
                WHERE code IN (
                    SELECT course_code 
                    FROM studentsReg
                    WHERE 
                        student_id = %s AND
                        status = 'enrolled'
                )
            """)
            self.__db_cursor(query, (student_id,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_course_scores(self, student_id):
        try:
            query = ("""
                SELECT name, code, instructor, capacity, (
                        SELECT status
                        FROM studentReg
                        WHERE studentReg.course_code = courses.code
                    ) AS status
                FROM courses
                WHERE code IN (
                    SELECT course_code 
                    FROM studentsReg
                    WHERE 
                        student_id = %s AND
                        status = 'enrolled'
                )
            """)
            self.__db_cursor.execute(query, (student_id,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    # Returns True if the student has passed the prerequisites of a course
    def passed_prerequisites_of_course(self, student_id, course_code):
        try:
            query = ("""
                SELECT NOT (
                    SELECT COUNT(*)
                        FROM coursePrerequisites
                        WHERE 
                            coursePrerequisites.course = %s AND 
                            NOT EXISTS (
                                SELECT course_code
                                FROM studentsReg
                                WHERE
                                    studentsReg.student_id = %s AND
                                    studentsReg.course_code = %s AND
                                    status = 'passed'
                            )
                )
            """)
            data = (course_code, student_id, course_code)
            self.__db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def is_course_available(self, code):
        try:
            query = ("""
                SELECT available
                FROM courses
                WHERE code = %s
            """)
            self.__db_cursor.execute(query, (code,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_course_schedule(self, course_code):
        try:
            query = ("""
                SELECT start_time, end_time, days 
                FROM courseSchedules 
                WHERE id IN (
                    SELECT schedule 
                    FROM courses 
                    WHERE code = %s
                )
            """)
            self.__db_cursor.execute(query, (course_code,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    # get the schedules of all the courses registered by a student
    def get_student_schedule(self, student_id):
        try:
            query = ("""
                SELECT start_time, end_time, days
                FROM courseSchedules
                WHERE id IN (
                    SELECT schedule
                    FROM courses c
                    LEFT JOIN studentsReg sr
                    ON c.code = sr.course_code
                    WHERE
                        sr.student_id = %s AND
                        sr.status = 'enrolled'
                )
            """)
            self.__db_cursor.execute(query, (student_id,))
        except Exception as e:
            print(str(e))
            return 'fail'
        return self.__db_cursor.fetchall()

    def get_student_name(self, student_id):
        try:
            query = ("""
                SELECT first_name, last_name
                FROM students
                WHERE id = %s
            """)
            self.__db_cursor.execute(query, (student_id,))
        except:
            print(str(e))
            return 'fail'      
        return self.__db_cursor.fetchall()
        
    def add_schedule(self, id, days, start_time, end_time, room_no):
        try:
            query = ("""
            INSERT INTO courseSchedules
            (id, days, start_time, end_time, room_no)
            VALUES
            (%s, %s, %s, %s, %s)
            """)
            data = (id, days, start_time, end_time, room_no)
            db_cursor.execute(query, data)
        except:
            print(str(e))
            return False    
        return True

    def add_course(self, code, name, description, instructor, capacity, schedule_id):
        try:
            query = ("""
                INSERT INTO courses
                (code, name, description, instructor, capacity, schedule)
                VALUES
                (%s, %s, %s, %s, %s, %s)
            """)
            data = (code, name, description, instructor, capacity, schedule_id)
            db_cursor.execute(query, data)
        except:
            print(str(e))
            return False    
        return True
            
    def add_prerequisites(self, course_code, prerequisite_code):
        try:
            query = ("""
                INSERT INTO coursePrerequisites
                (course, prerequisite_course)
                VALUES
                (%s, %s)
            """)
            data = (course_code, prerequisite_code)
            db_cursor.execute(query, data)
        except Exception as e:
            print(str(e))
            return False    
        return True

    # get courses ordered by the most popular
    def get_courses_most_popular(self):
        try:
            query = ("""
                SELECT c.name, c.code, c.instructor, COUNT(*) AS reg_count
                FROM courses c
                LEFT JOIN studentsReg sr
                ON c.code = sr.course_code
                GROUP BY c.code
                ORDER BY reg_count DESC
            """)
            self.__db_cursor.execute(query)
        except:
            print(str(e))
            return 'fail'      
        return self.__db_cursor.fetchall()

    # get courses ordered by the most enrolled
    def get_courses_most_enrolled(self):
        try:
            query = ("""
                SELECT c.name, c.code c.instructor, COUNT(*) AS enroll_count
                FROM courses c
                LEFT JOIN studentsReg sr
                ON c.code = sr.course_code
                WHERE sr.status = 'enrolled'
                GROUP BY c.code
                ORDER BY enroll_count DESC
            """)
            self.__db_cursor.execute(query)
        except:
            print(str(e))
            return 'fail'      
        return self.__db_cursor.fetchall()

    # get number of students enrolled into a course
    def course_students_count(self, course_code):
        try:
            query = ("""
                SELECT COUNT(*)
                FROM sudentsReg
                WHERE 
                    course_code = %s AND
                    status = 'enrolled'
            """)
            self.__db_cursor.execute(query, (course_code,))
        except:
            print(str(e))
            return 'fail'      
        return self.__db_cursor.fetchall()

    # Enroll student into course
    def register_course(self, student_id, course_code):
        try:
            query = ("""
                INSERT INTO studentsReg
                (student_id, course_code, status)
                VALUES
                (%s, %s, 'enrolled')
            """)
            data = (student_id, course_code)
            self.__db_cursor.execute(query, data)
        except:
            print(str(e))
            return False
        return True