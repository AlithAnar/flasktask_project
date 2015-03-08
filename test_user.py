# -*- coding: utf-8 -*-

import unittest

from utils import *



class UserTests(unittest.TestCase):
    def setUp(self):
        self.manager = TestManager()
        self.app = self.manager.get_app()
        db.create_all()
        self.assertEquals(app.debug, False)

    def tearDown(self):
        self.manager.tear_down()

    def test_user_setup(self):
        new_user = User('mherban', 'michale@mherman.org', 'passwords')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'mherban'


    def test_form_is_present_on_login_page(self):
        response = self.app.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please sign in to access your task list', response.data)


    def test_user_cannot_login_without_register(self):
        response = self.manager.login('foo', 'bar')
        self.assertIn('Invalid credentials', response.data)

    def test_user_can_login(self):
        self.manager.register('aaaaaaa', 'aaa@o2.pl', 'aaaaaaa', 'aaaaaaa')
        response = self.manager.login('aaaaaaa', 'aaaaaaa')
        self.assertIn('Legged in successfully', response.data)

    def test_invalid_form_data(self):
        self.manager.register('michael', 'michael@realpython.pl', 'python', 'python')
        response = self.manager.login('alert("alert box!', 'foo')
        self.assertIn('Invalid credentials', response.data)

    def test_form_present_on_register_page(self):
        response = self.app.get('users/register/')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Please register', response.data)

    def test_user_registration_error(self):
        self.app.get('users/register/', follow_redirects=True)
        self.manager.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.app.get('users/register/', follow_redirects=True)

        response = self.manager.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn('already taken', response.data)

    def test_logged_can_logout(self):
        self.manager.register('Michael', 'michael@realpython.com', 'python111', 'python111')
        self.manager.login('Michael', 'python111')
        response = self.manager.logout()

        self.assertIn('You have been logged out!', response.data)

    def test_not_logged_can_logout(self):
        response = self.manager.logout()
        self.assertNotIn('You have been logged out!', response.data)

    def test_user_registration_field_error(self):
        response = self.manager.register('Michael', 'michael@realpython.com', 'python111', '')
        self.assertIn('This field is required.', response.data)

    def test_default_user_role(self):
        db.session.add(User("Johny", "Johny@gmail.com", "johnny"))
        db.session.commit()
        users = db.session.query(User).all()
        for user in users:
            self.assertEquals(user.role, 'user')

    def test_hidden_links_for_no_task_owners(self):
        self.manager.register('Michael', 'michael@realpython.com', 'python111', 'python111')
        self.manager.login('Michael', 'python111')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.register(email='test@test.com', password='password123', confirm='password123', name='Bob')
        response = self.manager.login('Bob', 'password123')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.assertNotIn('MArk as complete', response.data)
        self.assertNotIn('Delete', response.data)

    def test_visible_links_for_task_owners(self):
        self.manager.register('Michael', 'michael@realpython.com', 'python111', 'python111')
        self.manager.login('Michael', 'python111')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.register(email='test@test.com', password='password123', confirm='password123', name='Bob')
        self.manager.login('Bob', 'password123')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.manager.create_task()
        self.assertIn('tasks/complete/2', response.data)
        self.assertIn('tasks/delete/2', response.data)

    def test_admin_can_see_everything(self):
        self.manager.register('Michael', 'michael@realpython.com', 'python111', 'python111')
        self.manager.login('Michael', 'python111')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.manager.create_task()
        self.manager.logout()
        self.manager.create_admin()
        self.manager.login('admin', 'password1')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.manager.create_task()
        self.assertIn('tasks/complete/1', response.data)
        self.assertIn('tasks/delete/1', response.data)
        self.assertIn('tasks/complete/2', response.data)
        self.assertIn('tasks/delete/2', response.data)

    def test_404_error(self):
        response = self.app.get('/not-exist')
        self.assertEquals(response.status_code, 404)
        self.assertIn('Sorry. Page not exists', response.data)


    def test_500_error(self):
        bad_user = User(name='Jeremy', email='jeremy@gmail.com', password='django')
        db.session.add(bad_user)
        db.session.commit()
        response = self.manager.login('Jeremy', 'django')
        self.assertEquals(response.status_code, 500)
        self.assertNotIn('ValueError: Invalid salt', response.data)
        self.assertIn('Something went wrong.', response.data)





if __name__ == '__main__':
    unittest.main()