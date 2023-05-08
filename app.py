from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./register.html')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)