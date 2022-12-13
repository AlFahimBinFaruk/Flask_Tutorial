from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# creating the server
server = Flask(__name__)

# creating the db
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
with server.app_context():
    db = SQLAlchemy(server)


# defining the db model/table of todo
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

# this path will server get and post req
@server.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        task_content = request.form['task']
        new_task = Todo(task=task_content)
        
        # add to db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "Some error occured."    
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks = tasks)    

# delete todo
@server.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Some error occured."       

# update todo
@server.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        # update the prev task
        task.task = request.form["task"]
        db.session.commit()
        return redirect("/")
    else:
        return render_template("update.html",task=task)    



# Running the server.
if __name__ == "__main__":
    server.run(debug=True)    