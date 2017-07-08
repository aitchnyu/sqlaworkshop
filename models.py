from sqlalchemy import ForeignKey, Enum, Sequence
from sqlalchemy.orm import relationship, backref

from extensions import db


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<Person {} {}>'.format(self.id, self.name)

    def __init__(self, name):
        self.name = name


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer)
    person_id = db.Column(db.Integer, ForeignKey('person.id'), index=True)

    person = relationship('Person', foreign_keys=[person_id])

    def __repr__(self):
        return '<Order {} {} {}>'.format(self.id, self.name, self.price)

    def __init__(self, person, name, price):
        self.person = person
        self.name = name
        self.price = price

# project and project user


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    admin_username = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<Project id:{} {}>'.format(self.id, self.name)

    def __init__(self, name, admin_username):
        self.name = name
        self.admin_username = admin_username


class ProjectUser(db.Model):
    __tablename__ = 'project_user'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, ForeignKey('project.id'), index=True)
    username = db.Column(db.String(), nullable=False)

    project = relationship('Project', foreign_keys=[project_id])

    def __repr__(self):
        return '<ProjectUser {} {}>'.format(self.project, self.username)

    def __init__(self, project, username):
        self.project = project
        self.username = username