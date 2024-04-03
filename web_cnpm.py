from flask import Flask, request, render_template, redirect
from sql import *

app = Flask(__name__)

@app.route('/')
def init():
    return render_template('index.html')
    
@app.route('/login', methods=['POST'])
def login():
    acc = request.form.get('account')
    pas = request.form.get('password')
    check = User(acc,pas).user_login
    if check is not None:
        return redirect("/home")
    return render_template('index.html') 

@app.route('/register', methods=['POST'])
def register():
    first = request.form.get('First_name')
    last = request.form.get('Last_name')
    name = str(first) + " " + str(last)
    acc = request.form.get('account_2')
    pas = request.form.get('password_2')
    email = request.form.get('number')
    user = User(acc, pas,name, email)
    check = user.user_register
    print(check)
    return render_template('index.html', check = check)
    
    

@app.route('/home')
def home():
    # return response for /home page
    pass

if __name__ == '__main__':
    app.run(debug=True)