import unittest

from flask import url_for
from app import create_app, db
from app.models import User


class FlaskTestClientCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Dump Your Brain' in response.get_data(as_text=True))

    def test_404_page(self):
        response = self.client.get('/non-existent-page')
        self.assertTrue('Not Found' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # register a new account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'test@example.com',
            'username': 'test',
            'password': 'test',
            'password2': 'test'
        })
        self.assertTrue(response.status_code == 302)

        # Attempt to register with same email
        response = self.client.post(url_for('auth.register'), data={
            'email': 'test@example.com',
            'username': 'same_email',
            'password': 'test',
            'password2': 'test'
        })
        data = response.get_data(as_text=True)
        self.assertTrue(
            'Email already registered.'
            in data)

        # Attempt to register with same username
        response = self.client.post(url_for('auth.register'), data={
            'email': 'same_username@example.com',
            'username': 'test',
            'password': 'test',
            'password2': 'test'
        })
        data = response.get_data(as_text=True)
        self.assertTrue(
            'Username already in use.'
            in data)

        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'test'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have not confirmed your account yet' in data)

        # login with wrong credentials
        response = self.client.post(url_for('auth.login'), data={
            'email': 'test@example.com',
            'password': 'wrong password'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('Invalid username or password' in data)

        # send a confirmation token
        user = User.query.filter_by(email='test@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(
            url_for('auth.confirm', token=token),
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)

        # log out
        response = self.client.get(
            url_for('auth.logout'),
            follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)
