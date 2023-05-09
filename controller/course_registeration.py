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
        if(first_name == '' or last_name == '' or email == '' or password == ''):
            return 'Please make sure to fill all the form fields'

        # verify names are text only
        if(not first_name.isalpha() or not last_name.isalpha()):
            return 'Student name should consist of alphabet letters only!'

        # check if user already exists
        if(get_student_id(email) != 'fail'):
            return 'There is already a Student account registered with this email'

        # Create hashed Password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

        # Create user in DB
        if not self.__course_reg_model.create_student(first_name, last_name, email, hashed_password):
            return 'Failed to create Student Account'

        return 'success'

    def login(self, data):
        email = data['email'].replace(' ', '')
        password = data['password']

        # get student from DB
        student = self.__course_reg_model.get_student_password(email)

        # db error
        if student == 'fail':
            return 'fail', 'Failed to Login'

        # check if student exists
        if student == []:
            return 'fail', 'There is not user registered with the provided email'

        student_password = student[0][0]

        # check if password is valid
        if not bcrypt.checkpw(password, student_password):
            return 'fail', 'Invalid Password'

        # Create cookie
        student_id = self.__course_reg_model.get_student_id(email)[0][0]
        cookie = self.create_session(student_id)
        if cookie == 'fail':
            return 'fail', 'Failed to create a session'

        # return cookie
        return 'success', cookie
    
    def create_session(self, student_id):
        cookie = secrets.token_hex(16)
        expiration_date = datetime.now() + timedelta(days=1)
        res = self.__course_reg_model.create_session(student_id, cookie, expiration_date)
        print(res)
        if not res:
            return 'fail'
        return cookie

    def verifySession(selfcookie):
        # if(cookie )
        pass