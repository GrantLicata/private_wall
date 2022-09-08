from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user
from flask_app.models import message
from datetime import datetime
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
    if not user.User.validate_user(request.form): 
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = user.User.save(data)
    return redirect('/wall')

# ||| Basic Login ||| -> Accepts and validates both the users email and password
@app.route('/login', methods=['POST'])
def login():
    print("---> Form data:", request.form)
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/wall")

# ||| Application Entry Point ||| -> Home page following authentication
@app.route('/wall')
def profile():
    if session == {}:
        return redirect('/')
    print("This should be an intiger:", session["user_id"])
    data = {
        "receiver_id": session["user_id"]
    }
    list_of_received_messages = message.Message.get_messages_by_receiver_id(data)
    received_count = 0
    for i in list_of_received_messages:
        received_count += 1
    message_data = {
        "id": session["user_id"]
    }
    list_of_sent_messages = user.User.get_all_sent_messages_by_id(message_data)
    sent_count = 0
    for i in list_of_sent_messages:
        sent_count += 1

    # Date difference calculations
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)

    return render_template("wall.html", all_users = user.User.get_all(), all_messages = list_of_received_messages, incoming_message_count = received_count, sent_message_count = sent_count, current_time = dt_string)

# ||| Basic Logout ||| -> Session data is cleared
@app.route('/logout')
def clear_session():
    session.clear()
    print("||-- Session should be clear --|| <> Session is:", session)
    return render_template("login.html")

# Sending messages to recipients
@app.route('/send_message', methods=["POST"])
def create():
    print("---> Form data:", request.form)
    data = {
        "receiver_id": request.form["user_id"],
        "user_id": session["user_id"],
        "message": request.form["message"]
    }
    if not user.User.validate_message(request.form): 
        return redirect('/wall')
    message.Message.send_message(data)
    return redirect('/wall')

#  Deleting messages
@app.route('/delete_message', methods=["POST"])
def delete():
    print("---> Form data:", request.form)
    data = {
        "id": request.form["message_id"]
    }
    message.Message.delete_message(data)
    return redirect('/wall')