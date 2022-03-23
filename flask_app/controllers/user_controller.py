from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User

@app.route("/")
def index():
    return render_template("index.html")

#=============================================
#Register Route
#=============================================

@app.route("/register", methods=["POST"])
def register_user():
    #1 -- validate form info
    if not User.validate_register(request.form):
        return redirect("/")

    #2 aside, convert password by bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    #2 - collect data from form
    query_data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
        
    }

    #3 - run query to database (INSERT) or you can say call on query from our model file
    new_user_id = User.create_user(query_data)

    #3A - add user id to session
    session["user_id"] = new_user_id


    #4 - redirect elsewhere
    return redirect("/")

#=============================================
#Login Route
#=============================================

@app.route("/login", methods= ["POST"])
def login():
    

    #1 -- validate form info
    if not User.validate_login(request.form):
        return redirect("/")
        

    #2 - query based on data
    query_data = {
        "email": request.form["email"]
    }
    logged_in_user = User.get_by_email(query_data)

    #3 - put user_id into session
    session["user_id"] = logged_in_user.id

    #4 - redirect elsewhere
    return redirect("/dashboard")

#=============================================
#Dashboard
#=============================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login or register before entering site!")
        return redirect("/")
    #pull id from session
    user_id = session["user_id"]
    return render_template("dashboard.html", logged_user_id = user_id)

#=============================================
#Logout
#=============================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")