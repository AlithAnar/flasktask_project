# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
import os

from project import app, db, bcrypt
from config import basedir
from project.models import User

TEST_DB = 'test.db'

class TestManager():
    def __init__(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tear_down(self):
        db.drop_all()

    def get_app(self):
        return self.app

    def login(self, name, password):
        return self.app.post('/users/', data=dict(name=name, password=password), follow_redirects=True)

    def register(self, name='Michael', email='michael@realpython.com', password='python111', confirm='python111'):
        return self.app.post('users/register/', data=dict(name=name, email=email, password=password, confirm=confirm),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('users/logout/', follow_redirects=True)

    def create_user(self, name="Michael", email="Michael@gmail.com", password="password1"):
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

    def create_admin(self):
        new_user = User(name="admin", email="admin@gmail.com", password=bcrypt.generate_password_hash("password1"), role="admin")
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('tasks/add/', data=dict(name='Go to the bank', due_date='02/02/2015', priority='1',
                                               posted_date='02/02/2015', status='1'), follow_redirects=True)