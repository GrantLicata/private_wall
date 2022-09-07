from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from pprint import pprint
bcrypt = Bcrypt(app)

# ||| Applicaiton Root ||| -> Most likely to be login & registration
@app.route("/")
def index():
    return render_template("login.html")

#||| Basic Registration ||| -> Generating a new user and giving them access to the application
@app.route('/register', methods=["POST"])
def register():
    print("---> Form data:", request.form)
    if not User.validate_user(request.form): 
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.save(data)
    return redirect('/')

# ||| Basic Login ||| -> Accepts and validates both the users email and password
@app.route('/login', methods=['POST'])
def login():
    print("---> Form data:", request.form)
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/")