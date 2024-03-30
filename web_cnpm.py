from flask import Flask, request, render_template, redirect
from sql import *

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login_check():
    user = User(request.form.get('account'), request.form.get('password'))
    if user.user_login() is not None:                                          
        return redirect('/home')
    else:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    user = User(request.form.get('username'), request.form.get('password'))
    if request.method == 'GET':
        return render_template('register.html')
    if user.user_register() == True:
        return redirect('/login')
    return render_template('register.html')

@app.route('/home')
def home():
    # return response for /home page
    pass

if __name__ == '__main__':
    app.run(debug=True)