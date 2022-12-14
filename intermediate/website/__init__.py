from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "test.db"

# create app
def create_app():
    app = Flask(__name__)
    # this will encrypt the session and cookies realted data in our website.
    app.config["SECRET_KEY"] = "faoll3l55l3l344mm5ll"
    
    # configuring db
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app=app)

    # registers blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/auth")

    # creating db(if not exits)
    from .model import Note,User
    create_db(app)

    # making a login managers to handle sessinons
    login_manager=LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_db(app):
    if not path.exists("instance/"+DB_NAME):
        app.app_context().push()
        db.create_all()
        print("New DB Created.")
