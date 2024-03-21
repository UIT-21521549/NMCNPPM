from flask import Flask, request, render_template, redirect
from sql import *

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login_check():
    username = request.form.get('username')
    password = request.form.get('password')
    action = request.form.get('action')
    action2 = request.form.get('01')
    if action == 'Đăng nhập':
        if user_login(username, password) is not None:                                          
            return redirect('/home')
        else:
            return render_template('index.html')
    elif  action == "Đăng ký" and action2 is None:
        return redirect('/register')
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'GET':
        return render_template('register.html')
    if user_register(username, password) == True:
        return redirect('/login')
    return render_template('register.html')

@app.route('/home')
def home():
    # return response for /home page
    pass

if __name__ == '__main__':
    app.run(debug=True)