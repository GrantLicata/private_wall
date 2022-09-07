#-------------------------------------------------------------------
from flask import render_template, redirect, request, session, flash
from pprint import pprint
from flask_app import app
#-------------------------------------------------------------------

# ||| Applicaiton Root ||| -> Most likely to be login & registration
@app.route("/")
def index():
    return render_template("index.html")

# ||| Simple post route ||| -> Sending form data into a database
@app.route('/NAME-ROUTE', methods=["POST"])
def create():
    print("---> Form data:", request.form)
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"]
    }
    User.save(data)
    return redirect('/NAME-ROUTE')

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
        "password" : bcrypt.generate_password_hash(request.form['password']),
        "birthday" : request.form["birthday"],
        "gender" : request.form["gender"],
        "language" : request.form["language"]
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

# ||| Basic Logout ||| -> Session data is cleared
@app.route('/clear')
def clear_session():
    session.clear()
    print("||-- Session should be clear --|| <> Session is:", session)
    return render_template("logreg.html")

# ||| Application Entry Point ||| -> Home page following authentication
@app.route('/profile')
def profile():
    if session == {}:
        return redirect('/')
    return render_template("/")