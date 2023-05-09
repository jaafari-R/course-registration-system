from flask import Flask, request, render_template
from controller.course_registeration import CourseRegisterationController
from model.course_registration import CourseRegisterationModel

app = Flask(__name__)
course_reg_model = CourseRegisterationModel()
course_reg_controller = CourseRegisterationController(course_reg_model)


@app.route('/')
def index():
    return 'Hello'

@app.route('/signup', methods=['GET'])
def register_form():
    return render_template('./register.html')

@app.route('/signup', methods=['POST'])
def register():
    res = course_reg_controller.register_student(request.form)
    if(res != 'success'):
        return res
    return "ok"

@app.route('/signin', methods=['GET'])
def login_form():
    return render_template('./login.html')

@app.route('/signin', methods=['POST'])
def login():
    return 'ok'


if __name__ == "__main__":
    app.run(debug=True)