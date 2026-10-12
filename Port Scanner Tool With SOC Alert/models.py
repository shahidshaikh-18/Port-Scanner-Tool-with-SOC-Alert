from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __bind_key__ = "users_db"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)


class SOCAlert(db.Model):
    __bind_key__ = "alerts_db"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(300), nullable=False)