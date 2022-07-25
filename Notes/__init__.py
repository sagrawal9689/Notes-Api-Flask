from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjashkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .note import note
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(note, url_prefix='/notes')

    return app