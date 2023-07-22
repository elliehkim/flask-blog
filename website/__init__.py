from flask import Flask
from flask_login import LoginManager
from .models import User
from bson.objectid import ObjectId
from .db import db

users = db.user
posts = db.blog_collection
enquiries = db.enquiry

def create_app():
    app = Flask(__name__)
    app.secret_key = "helloworld"

    from .auth import auth
    from .views import views


    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(_id):
        user = users.find_one({'_id': ObjectId(_id)})
        if not user:
            return None
        return User(user['username'], user['email'], user['password'], str(user['_id']))

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app