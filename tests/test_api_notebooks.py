import json
from flask import url_for
from api_base import ApiBaseTestCase


class NotebookApiTestCase(ApiBaseTestCase):

    def test_get_all_noteboooks(self):
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.headers)
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue('notebooks' in json_response)

    def test_create_notebook(self):
        response = self.client.post(
            url_for('api.notebooks'),
            headers=self.headers,
            data=json.dumps({
                "title": "Test Notebook Title"
            }))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response.status_code == 201)
        self.assertEqual(
            'Test Notebook Title', json_response['notebook']['title'])
