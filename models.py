from app import db, app
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_salt, make_hash, check_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    post = db.relationship("Post", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_hash(password)
