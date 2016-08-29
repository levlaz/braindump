import json
from flask import url_for
from api_base import ApiBaseTestCase


class AuthApiTestCase(ApiBaseTestCase):

    def test_basic_auth(self):
        self.add_user()

        # Issue Request with Basic Auth
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.set_auth_headers('test@example.com', 'password'))
        self.assertTrue(response.status_code == 200)

        # Issue Request with Bad Username
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.set_auth_headers('bad@example.com', 'password'))
        self.assertTrue(response.status_code == 401)

        # Issue Request with Bad Password
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.set_auth_headers('test@example.com', 'bad'))
        self.assertTrue(response.status_code == 401)

        # Issue Request with Bad Username and Password
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.set_auth_headers('bad@example.com', 'bad'))
        self.assertTrue(response.status_code == 401)

    def test_token_auth(self):
        self.add_user()

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
