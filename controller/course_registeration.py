import bcrypt # for password hashing & salt


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

        # Create hashed Password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

        print(hashed_password, len(hashed_password))

        # Create user in DB
        if(not self.__course_reg_model.create_student(first_name, last_name, email, hashed_password)):
            return 'Failed to create Student Account'

        return 'success'