from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "database.db"

#password = 12345678

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']  = 'jrgkvnjekg kjnewfnjgbjwekrgb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .view import view_bp
    from .auth import auth


    app.register_blueprint(view_bp, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from website.models import User, Note
    create_database(app)


    return app 


def create_database(app):
    # Ensure the DB file path is correct (project root) and create tables
    if not path.exists(DB_NAME):
        # create_all requires an application context in recent Flask-SQLAlchemy
        with app.app_context():
            db.create_all()
        print('Created Database!')