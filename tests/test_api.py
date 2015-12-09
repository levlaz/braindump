import unittest
import json
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models import User


class APITestCase(unittest.TestCase):

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

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('email', 'password'))
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(
            response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')

    def test_no_auth(self):
        response = self.client.get(
            url_for('api.get_notes'),
            content_type='application/json')
        self.assertTrue(response.status_code == 401)

    def test_bad_auth(self):
        # add a user
        u = User(email='test@example.com', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # attempt to authenticate with bad password
        response = self.client.get(
            url_for('api.get_notes'),
            headers=self.get_api_headers(
                'test@example.com', 'wrong password'))
        self.assertTrue(response.status_code == 401)

    def test_token_auth(self):
        # add a user
        u = User(email='test@example.com', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # issue request with bad token
        response = self.client.get(
            url_for('api.get_notes'),
            headers=self.get_api_headers('bad-token', ''))
        self.assertTrue(response.status_code == 401)

        # get a token
        response = self.client.get(
            url_for('api.get_token'),
            headers=self.get_api_headers('test@example.com', 'password'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(
            response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the new token
        response = self.client.get(
            url_for('api.get_notes'),
            headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)

    def test_anonymous(self):
        # Try to get notes
        response = self.client.get(
            url_for('api.get_notes'),
            headers=self.get_api_headers('', ''))
        self.assertTrue(response.status_code == 401)

        # Try to get a token
        response = self.client.get(
            url_for('api.get_token'),
            headers=self.get_api_headers('', ''))
        self.assertTrue(response.status_code == 401)

    def test_unconfirmed_acount(self):
        # add an unconfirmed user
        u = User(
            email='test@example.com',
            password='password2',
            confirmed=False)
        db.session.add(u)
        db.session.commit()

        # get notes from unconfirmed account
        response = self.client.get(
            url_for('api.get_notes'),
            headers=self.get_api_headers(
                'test@example.com', 'password2'))
        self.assertTrue(response.status_code == 403)
