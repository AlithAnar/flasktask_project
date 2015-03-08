# -*- coding: utf-8 -*-

import unittest

from utils import *


class TasksTests(unittest.TestCase):
    def setUp(self):
        self.manager = TestManager()
        self.app = self.manager.get_app()
        db.create_all()
        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.drop_all()

    def test_logged_can_access_task(self):
        self.manager.register('Michael', 'michael@realpython.com', 'python111', 'python111')
        self.manager.login('Michael', 'python111')
        response = self.app.get('tasks/tasks/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Add a new task', response.data)


    def test_not_logged_can_access_task(self):
        response = self.app.get('tasks/tasks/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Login first', response.data)

    def test_user_can_add_task(self):
        self.manager.create_user('Michael', 'Michael@gmail.com', 'password1')
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.manager.create_task()
        self.assertIn('New entry added succesfully', response.data)

    def test_user_cannot_add_task_when_error(self):
        self.manager.create_user('Michael', 'Michael@gmail.com', 'password1')
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.app.post('tasks/add/', data=dict(name='Go to the bank', due_date='', priority='1',
                                               posted_date='02/02/2015', status='1'), follow_redirects=True)
        self.assertIn('Not valid data in form!', response.data)

    def test_user_can_complete_task(self):
        self.manager.create_user('Michael', 'Michael@gmail.com', 'password1')
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        response = self.app.get('tasks/complete/1/', follow_redirects=True)
        self.assertIn('Task marked as complete', response.data)

    def test_user_can_delete_task(self):
        self.manager.create_user()
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        response = self.app.get('tasks/delete/1/', follow_redirects=True)
        self.assertIn('Task deleted', response.data)

    def test_user_cannot_complete_others_tasks(self):
        self.manager.create_user()
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.create_user(name="Michael2", email="Michael2@gmail.com")
        self.manager.login('Michael2', 'password1')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('tasks/complete/1/', follow_redirects=True)
        self.assertIn('Not permitted', response.data)

    def test_user_cannot_delete_others_tasks(self):
        self.manager.create_user()
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.register(name="Michael3", email="Michael3@gmail.com", password="password1", confirm="password1")
        self.manager.login('Michael3', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.app.get('tasks/delete/1/', follow_redirects=True)
        self.assertIn('Not permitted', response.data)


    def test_admin_can_complete_others_tasks(self):
        self.manager.create_user()
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.create_admin()
        self.manager.login('admin', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.app.get('tasks/complete/1/', follow_redirects=True)
        self.assertNotIn('Not permitted', response.data)

    def test_admin_can_delete_others_tasks(self):
        self.manager.create_user()
        self.manager.login('Michael', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.create_admin()
        self.manager.login('admin', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.app.get('tasks/delete/1/', follow_redirects=True)
        self.assertNotIn('Not permitted', response.data)

    def test_task_template_displays_username(self):
        self.manager.register('Michael', 'michael@realpython.com', 'python111', 'python111')
        self.manager.login('Michael', 'python111')
        response = self.app.get('tasks/tasks/', follow_redirects=True)
        self.assertIn('Michael', response.data)

if __name__ == '__main__':
    unittest.main()