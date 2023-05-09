from model.db_connect import db_con

class CourseRegisterationModel:
    def __init__(self):
        self.__db_cursor = db_con.cursor()

    # TODO
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

    # TODO
    def get_student(self):
        pass

    # TODO
    def create_course(self):
        pass

    # TODO
    def get_courses(self):
        pass

    # TODO
    def search_courses(self, course_code, course_name, course_instructor):
        pass
