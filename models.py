import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "ethiopia_database"
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", "", "localhost:5432", database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# create contact table
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    branch = db.Column(db.String(1000))
    city = db.Column(db.String(1000))
    kifle_ketema = db.Column(db.String(1000))
    direction = db.Column(db.String(1000))
    building = db.Column(db.String(1000))
    flat = db.Column(db.String(1000))
    phone = db.Column(db.String(1000))

    def __init__(self, name, branch=None, city=None, kifle_ketema=None, direction=None, building=None, flat=None, phone=None):
        self.name = name
        self.branch = branch
        self.city = city
        self.kifle_ketema = kifle_ketema
        self.direction = direction
        self.building = building
        self.flat = flat
        self.phone = phone


    def __repr__(self):
        return '<Contact %r>' % self.name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'branch': self.branch,
            'city': self.city,
            'kifle_ketema': self.kifle_ketema,
            'direction': self.direction,
            'building': self.building,
            'flat': self.flat,
            'phone': self.phone,
        }
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'branch': self.branch,
            'city': self.city,
            'kifle_ketema': self.kifle_ketema,
            'direction': self.direction,
            'building': self.building,
            'flat': self.flat,
            'phone': self.phone,
        }

