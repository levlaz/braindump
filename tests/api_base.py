import unittest
import json
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models import User


class ApiBaseTestCase(unittest.TestCase):

    @property
    def headers(self):
        return self.set_token_headers(self.get_auth_token())

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def set_auth_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def set_token_headers(self, token):
        return {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_auth_token(self):
        # Add new user
        u = User(email='test@example.com', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        response = self.client.get(
            url_for('api.token'),
            headers=self.set_auth_headers('test@example.com', 'password'))

        json_response = json.loads(
            response.data.decode('utf-8'))

        return json_response['token']
