# -*- coding: utf-8 -*-
import unittest
from datetime import date

from utils import TestManager
from project import app, db
from project.models import Task


TEST_DB = 'test.db'


class MainTests(unittest.TestCase):
    def setUp(self):
        self.m = TestManager()
        self.app = self.m.get_app()
        db.create_all()
        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_tasks(self):
        db.session.add(
            Task("run around in circles",
                 date(2015, 1, 22),
                 10,
                 1,
                 1,
                 date(2015, 1, 05)
                 ))
        db.session.commit()

        db.session.add(
            Task("purchase real python",
                 date(2015, 1, 12),
                 10,
                 1,
                 1,
                 date(2015, 1, 05)
                 ))
        db.session.commit()

    def test_collection_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/tasks/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn('run around in circles', response.data)
        self.assertIn('purchase real python', response.data)

    def test_resource_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/tasks/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn('purchase real python', response.data)
        self.assertNotIn('run around in circles', response.data)

    def test_invalid_resource_endpoind_returns_error(self):
        self.add_tasks()
        response = self.app.get('api/tasks/222', follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn('Element does not exist', response.data)


if __name__ == '__main__':
    unittest.main()

