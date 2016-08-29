import json
from flask import url_for
from app import db
from app.models import User
from api_base import ApiBaseTestCase


class AuthApiTestCase(ApiBaseTestCase):

    def test_token_auth(self):
        # add a user
        u = User(email='test@example.com', password='password', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # get a token
        response = self.client.get(
            url_for('api.token'),
            headers=self.set_auth_headers('test@example.com', 'password'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(
            response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the new token
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.set_token_headers(token))
        self.assertTrue(response.status_code == 200)
        self.assertTrue('notebooks' in response.get_data(as_text=True))
