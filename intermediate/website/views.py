# This will handle the POST,GET,DELETE,UPDATE req for notes
from flask import Blueprint,request,render_template,flash,redirect
from flask_login import current_user,login_required
from .model import Note
from . import db

views = Blueprint("views",__name__)

# handle add new task and get req.
@views.route("/",methods=["POST","GET"])
@login_required
def home():
    if request.method == "POST":
        data = request.form.get("data")

        if not data:
            flash("Too short a add",category="danger")
        else:
            newNote=Note(data=data,user_id=current_user.id)
            db.session.add(newNote)
            db.session.commit()
            flash("Note added",category="success")
            return redirect("/")

    return render_template("home.html",user=current_user)    

# handle update 
@views.route("/update/<int:id>",methods=["POST","GET"])
def update(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        note.data=request.form.get("data")
        db.session.commit()
        flash("note updated.",category="success")
        return redirect("/")
    else:
        return render_template("update.html",user=current_user,note=note)    

# handle delete
@views.route("/delete/<int:id>")
def delete(id):
    noteToDelete = Note.query.get_or_404(id)

    try:
        db.session.delete(noteToDelete)
        db.session.commit()
        return redirect("/")  
    except:
        flash("some error occured.",category="danger")          