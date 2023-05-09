from flask import Flask, request, render_template, make_response, redirect, url_for

from controller.course_registeration import CourseRegisterationController
from model.course_registration import CourseRegisterationModel

app = Flask(__name__)
course_reg_model = CourseRegisterationModel()
course_reg_controller = CourseRegisterationController(course_reg_model)




@app.route('/')
def index():
    cookie = request.cookies.get('course_reg')
    if not course_reg_controller.verifySession(cookie):
        return redirect(url_for('login_form'))

    return 'Hello'


@app.route('/signup', methods=['GET'])
def register_form():
    cookie = request.cookies.get('course_reg')
    if course_reg_controller.verifySession(cookie):
        return redirect(url_for('index'))

    return render_template('./register.html')


@app.route('/signin', methods=['GET'])
def login_form():
    cookie = request.cookies.get('course_reg')
    if course_reg_controller.verifySession(cookie):
        return redirect(url_for('index'))
    return render_template('./login.html')


@app.route('/signup', methods=['POST'])
def register():
    status, cookie, exp_date = course_reg_controller.register_student(request.form)

    # failed to login
    if(status == 'fail'):
        return cookie
    
    res = make_response(redirect(url_for('index')))
    res.set_cookie('course_reg', value=cookie, expires=exp_date)
    return res
    

@app.route('/signin', methods=['POST'])
def login():
    status, cookie, exp_date = course_reg_controller.login(request.form)
    
    # failed to login
    if(status == 'fail'):
        return cookie
    
    res = make_response(redirect(url_for('index')))
    res.set_cookie('course_reg', value=cookie, expires=exp_date)
    return res


if __name__ == "__main__":
    app.run(debug=True)