# This will handle login,signup,logout related req.
from flask import Blueprint, render_template, request, flash, redirect
from .model import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__)

# Handle login route
@auth.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # check if user eixts
        user = User.query.filter_by(email=email).first()
        if user:
            # if exits match password
            if check_password_hash(user.password, password):
                flash("login successful", category="success")
                login_user(user, remember=True)
                return redirect("/")
            else:
                flash("incorrect cred", category="danger")

        else:
            flash("incorrect cred", category="danger")

    
    return render_template("login.html",user=current_user)


# handle signup routes
@auth.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # if user with email alrady exits we will not create one.
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exits.",category="danger")
        # see if everything is correct.    
        elif not name or not email or not password:
            flash("Provide every input value",category="danger")    
        else:
            # if everything is correct then create a new one
            new_user = User(email=email,name=name,password=generate_password_hash(password,method="sha256"))
            # add it to db
            db.session.add(new_user)    
            db.session.commit()
            # login the new user from here
            login_user(new_user,remember=True)
            flash("Account created.",category="success")
            return redirect("/")
    
    return render_template("signup.html",user=current_user)    

# handle logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/auth")