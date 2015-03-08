# -*- coding: utf-8 -*-
from datetime import date

from project import db
from project.models import Task, User

db.create_all()

# db.session.add(User("admin", "ad@min.com", "admin", "admin"))
# db.session.add(User("username", "username@min.com", "username", "user"))

db.session.add(Task("Finish course", date(2014, 3, 13), 10, 1, 1, date(2014, 3, 13)))

db.session.commit()