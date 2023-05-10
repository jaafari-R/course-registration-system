from flask import Flask, request, render_template, make_response, redirect, url_for

from controller.course_registeration import CourseRegisterationController
from model.course_registration import CourseRegisterationModel

app = Flask(__name__)
course_reg_model = CourseRegisterationModel()
course_reg_controller = CourseRegisterationController(course_reg_model)



def verify_session(request):
    cookie = request.cookies.get('course_reg')
    return course_reg_controller.verifySession(cookie)

def close_session(request):
    cookie = request.cookies.get('course_reg')
    course_reg_controller.closeSession(cookie)


# view All courses
@app.route('/')
def index(): 
    if not verify_session(request):
        return redirect(url_for('login_form'))

    status, courses = course_reg_controller.search_courses(request.args)
    
    if(status == 'fail'):
        return courses

    return render_template('./courses.html', courses=courses)

# view enrollable courses
@app.route('/courses/register', methods=['GET'])
def register_courses():
    if not verify_session(request):
        return redirect(url_for('login_form'))

    status, courses = course_reg_controller.search_enrollable_courses(request.cookies.get('course_reg'), request.args)
    
    if(status == 'fail'):
        return courses

    return render_template('./courses.html', courses=courses, register=True)

# view a single course
@app.route('/courses', methods=['GET'])
def single_course():
    if not verify_session(request):
        return redirect(url_for('login_form'))

    status, course, prerequisites = course_reg_controller.get_course(request.args)

    if(status == 'fail'):
        return course

    print(course)
    return render_template('./course.html', course=course, prerequisites=prerequisites)

# student register into a cours
@app.route('/course/register', methods=['POST'])
def register_course():
    if not verify_session(request):
        return redirect(url_for('login_form'))


# -- Student Registration / Login / Logout -- #

@app.route('/signup', methods=['GET'])
def register_form():
    if verify_session(request):
        return redirect(url_for('index'))

    return render_template('./register.html')


@app.route('/signin', methods=['GET'])
def login_form():
    if verify_session(request):
        return redirect(url_for('index'))

    return render_template('./login.html')


@app.route('/signup', methods=['POST'])
def register():
    if verify_session(request):
        return redirect(url_for('index'))

    status, cookie, exp_date = course_reg_controller.register_student(request.form)

    # failed to login
    if(status == 'fail'):
        return cookie
    
    res = make_response(redirect(url_for('index')))
    res.set_cookie('course_reg', value=cookie, expires=exp_date)
    return res
    

@app.route('/signin', methods=['POST'])
def login():
    if verify_session(request):
        return redirect(url_for('index'))

    status, cookie, exp_date = course_reg_controller.login(request.form)
    
    # failed to login
    if(status == 'fail'):
        return cookie
    
    res = make_response(redirect(url_for('index')))
    res.set_cookie('course_reg', value=cookie, expires=exp_date)
    return res

@app.route('/signout', methods=['GET'])
def logout():
    # close session from server side
    close_session(request)
    # close session from client side & redirect to login page
    res = make_response(redirect(url_for('login_form')))
    res.delete_cookie('course_reg')
    return res


if __name__ == "__main__":
    app.run(debug=True)