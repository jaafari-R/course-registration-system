# for password hashing & salt
import random
import string
#

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

        # Create Salt and hashed Password
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        password_hash = hash(password + salt)

        # Create user in DB
        if(not self.__course_reg_model.create_student(first_name, last_name, email, password_hash, salt)):
            return 'Failed to create Student Account'

        return 'success'