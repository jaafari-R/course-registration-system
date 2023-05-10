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

    def get_course(self, data):
        course_code = data.get('code')

        course = self.__course_reg_model.get_course(course_code)
        prerequisites = self.__course_reg_model.get_course_prerequisites(course_code)

        if course == 'fail' or prerequisites == 'fail':
            return 'fail', 'Failed to retrieve course information', None

        if course == []:
            return 'fail', 'Course does not exist', None

        print(prerequisites)

        return 'success', course[0], prerequisites

    def register_course(self, cookie, data):
        course_code = data['course_code']
        student_id = self.__course_reg_model.get_session_student_id(cookie)

        if student_id == 'fail':
            return 'fail', 'Failed to register course'
        student_id = student_id[0][0]


        passed_prereq = self.__course_reg_model.passed_prerequisites_of_course(student_id, course_code)[0]
        if not passed_prereq:
            return 'fail', 'Failed to register course, you have not passed this course` prerequisites'

        course_available = self.__course_reg_model.is_course_available(course_code)[0]
        if not course_available:
            return 'fail', 'Failed to register course, the course is not available currently'


        course_schedule = self.__course_reg_model.get_course_schedule(course_code)
        student_courses_schedule = self.__course_reg_model.get_student_schedule(student_id)

        course_start_time = course_schedule[0][0]
        course_end_time = course_schedule[0][1]
        course_days = course_schedule[0][2]
        # check for clashing shcedules
        for sc_sch in student_courses_schedule:
            start_time = sc_sch[0]
            end_time = sc_sch[1]
            days = sc_sch[2]
            for day in days:
                if day in course_days:
                    if (start_time <= course_start_time <= end_time) or (start_time <= course_end_time <= end_time):
                        return 'fail', 'Failed to register course, Course schedule clashes with the schedule of already registered courses'

        # Register Course
        res = self.__course_reg_model.register_course(student_id, course_code)
        if not res:
            return 'fail', 'Failed to register course'

        return 'success', 'Course Registered Successfully'

    # return the courses the user is enrolled in
    def get_student_courses(self, cookie):
        student_id = self.__course_reg_model.get_session_student_id(cookie)

        if student_id == 'fail':
            return 'fail', 'Failed to retrieve course'
        student_id = student_id[0][0]

        courses = self.__course_reg_model.get_registered_courses(student_id)

        if courses == 'fail':
            return 'fail', 'Failed to retrieve course'

        return 'success', courses

    def get_courses_most_enrolled(self):
        courses = self.__course_reg_model.get_courses_most_enrolled()

        if courses == 'fail':
            return 'fail', 'Failed to retrieve most enrolled courses analysis'

        print(courses)

        return 'success', courses

    def get_courses_most_popular(self):
        courses = self.__course_reg_model.get_courses_most_popular()

        if courses == 'fail':
            return 'fail', 'Failed to retrieve most popular courses analysis'

        return 'success', courses

    def get_student_passed_courses(self, cookie):
        student_id = self.__course_reg_model.get_session_student_id(cookie)

        if student_id == 'fail':
            return 'fail', 'Failed to retrieve course'
        student_id = student_id[0][0]
        
        courses = self.__course_reg_model.get_passed_courses(student_id)

        return 'success', courses