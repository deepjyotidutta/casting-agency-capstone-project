import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "casting_agency"
    database_path = "postgres://{}/{}".format(
        'postgres:pass@localhost:5432', database_name)

db = SQLAlchemy()

'''
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_create_initialize():
    '''drops the database tables 
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''initialize test records for unittest'''
    new_actor = (Actor(
        name = 'Shahid Kapoor',
        gender = 'Male',
        age = 25
        ))
    new_movie = (Movie(
        title = 'Kabir Singh',
        release_date = '12/12/2021'
        ))
    new_actor.insert()
    new_movie.insert()
    new_moviecast = (MovieCast(
        movie_id = new_movie.id,
        actor_id = new_actor.id,
        role = 'Hero'
    ))
    new_moviecast.insert()


class MovieCast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    role = db.Column(db.String)

    def __init__(self, movie_id, actor_id, role):
        self.movie_id = movie_id
        self.actor_id = actor_id
        self.role = role

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.upda

    def format(self):
        return {
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'role': self.role}


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    cast = db.relationship('MovieCast', backref='movie', lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    cast = db.relationship('MovieCast', backref='actor', lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}
