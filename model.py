#encoding: utf-8

from exts import db
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash , check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.username = username
        self.password = generate_password_hash(password)
    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=dt.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=dt.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref=db.backref('answers'))
    question = db.relationship('Question',backref=db.backref('answers',order_by=id.desc()))