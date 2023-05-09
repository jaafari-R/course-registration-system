import bcrypt # for password hashing
import secrets
from datetime import datetime, timedelta


class CourseRegisterationController:
    def __init__(self, model):
        self.__course_reg_model = model

    def register_student(self, data):
        first_name = data['first_name'].replace(' ', '')
        last_name = data['last_name'].replace(' ', '')
        email = data['email'].replace(' ', '')
        password = data['password']

        # check if the is missing data
        if first_name == '' or last_name == '' or email == '' or password == '':
            return 'fail', 'Please make sure to fill all the form fields', None

        # verify names are text only
        if not first_name.isalpha() or not last_name.isalpha():
            return 'fail', 'Student name should consist of alphabet letters only!', None

        # check if user already exists
        student_id = self.__course_reg_model.get_student_id(email)
        if student_id == 'fail':
            return 'fail', 'Failed to login', None
        if student_id != []:
            return 'fail', 'There is already a Student account registered with this email', None

        # Create hashed Password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

        # Create user in DB
        if not self.__course_reg_model.create_student(first_name, last_name, email, hashed_password):
            return 'fail', 'Failed to create Student Account', None

        # Create session and get cookie
        student_id = self.__course_reg_model.get_student_id(email)[0][0]
        cookie, exp_date = self.create_session(student_id)
        if cookie == 'fail':
            return 'fail', 'Failed to create a session', None

        # return cookie
        return 'success', cookie, exp_date


    def login(self, data):
        email = data['email'].replace(' ', '')
        password = data['password']

        # get student from DB
        student = self.__course_reg_model.get_student_password(email)

        # db error
        if student == 'fail':
            return 'fail', 'Failed to Login', None

        # check if student exists
        if student == []:
            return 'fail', 'There is no user registered with the provided email', None

        student_password = student[0][0]

        # check if password is valid
        if not bcrypt.checkpw(password, student_password):
            return 'fail', 'Invalid Password', None

        # Create session and get cookie
        student_id = self.__course_reg_model.get_student_id(email)[0][0]
        cookie, exp_date = self.create_session(student_id)
        if cookie == 'fail':
            return 'fail', 'Failed to create a session', None

        # return cookie
        return 'success', cookie, exp_date
    
    def create_session(self, student_id):
        cookie = secrets.token_hex(16)
        expiration_date = datetime.now() + timedelta(days=1)
        
        res = self.__course_reg_model.create_session(student_id, cookie, expiration_date)
        if not res:
            return 'fail'
        
        return cookie, expiration_date

    def closeSession(self, cookie):
        if(cookie != None):
            self.__course_reg_model.delete_session(cookie)

    # return True when session is Valid, otherwise False
    def verifySession(self, cookie):
        if cookie == None:
            return False

        res = self.__course_reg_model.get_session_exp_date(cookie)
        
        if res == 'fail' or res == []: 
            return False

        # check if token has expired
        expiration_date = res[0][0]
        if datetime.now() > expiration_date:
            self.closeSession(cookie)
            return False

        return True

    def search_courses(self, data):
        course_code = data.get('course_code')
        course_name = data.get('course_name')
        course_instructor = data.get('course_instructor')

        # get all courses if no search options are specified
        if course_code == None and course_name == None and course_instructor == None:
            res = self.__course_reg_model.get_all_courses()
            if res == 'fail':
                return 'fail', 'Failed to retrieve courses'
            return 'success', res
        else:
            res = self.__course_reg_model.search_courses(course_code, course_name, course_instructor)
            if res == 'fail':
                return 'fail', 'Failed to retrieve courses'
            return 'success', res

    def get_student_id(self, cookie):
        res = self.__course_reg_model.get_session_student_id(cookie)
        
        if res == 'fail' or res == []:
            return 'fail'
        return res[0][0]


    def search_enrollable_courses(self, cookie, data):
        student_id = self.get_student_id(cookie)
        if(student_id == 'fail'):
            return 'Failed to retrieve courses'

        course_code = data.get('course_code')
        course_name = data.get('course_name')
        course_instructor = data.get('course_instructor')

        # get all courses if no search options are specified
        if course_code == None and course_name == None and course_instructor == None:
            res = self.__course_reg_model.get_enrollable_courses(student_id)
            if res == 'fail':
                return 'fail', 'Failed to retrieve courses'
            return 'success', res
        else:
            res = self.__course_reg_model.search_enrollable_courses(student_id, course_code, course_name, course_instructor)
            if res == 'fail':
                return 'fail', 'Failed to retrieve courses'
            return 'success', res