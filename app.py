from flask import Flask, request, render_template
from controller.course_registeration import CourseRegisterationController
from model.course_registration import CourseRegisterationModel

app = Flask(__name__)
course_reg_model = CourseRegisterationModel()
course_reg_controller = CourseRegisterationController(course_reg_model)


@app.route('/')
def index():
    return render_template('./register.html')

@app.route('/register', methods=['POST'])
def register():
    res = course_reg_controller.register_student(request.form)
    if(res != 'success'):
        return res
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)