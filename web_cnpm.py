from flask import Flask, request, render_template
from sql import *
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login_check():
    username = request.form.get('username')
    password = request.form.get('password')
    if user_login(username, password) is not None:
        return '<h2>123</h2>'
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
