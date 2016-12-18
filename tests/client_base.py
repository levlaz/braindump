import os
import app
import unittest
from app.models import User


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        app.db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()
        self.app_context.pop()

    def add_user(self):
        u = User(email='test@example.com', password='password', confirmed=True)
        app.db.session.add(u)
        app.db.session.commit()
        return u

    def add_other_user(self):
        u = User(
            email='other@example.com', password='password', confirmed=True)
        app.db.session.add(u)
        app.db.session.commit()
        return u

    def login(self, email, password):
        return self.client.post('/auth/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)