import json
from flask import url_for
from api_base import ApiBaseTestCase
from app import db
from app.models import Notebook


class NotebookApiTestCase(ApiBaseTestCase):

    def test_get_all_noteboooks(self):
        response = self.client.get(
            url_for('api.notebooks'),
            headers=self.headers)
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue('notebooks' in json_response)

    def test_create_notebook(self):
        # Will neeed to use headers twice
        local_headers = self.headers

        response = self.client.post(
            url_for('api.notebooks'),
            headers=local_headers,
            data=json.dumps({
                "title": "Test Notebook Title"
            }))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response.status_code == 201)
        self.assertEqual(
            'Test Notebook Title', json_response['notebook']['title'])

        # Test to make sure new notebook shows up in all notebooks
        response = self.client.get(
            url_for('api.notebooks'),
            headers=local_headers)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            'Test Notebook Title' in response.get_data(as_text=True))

    def test_create_notebook_with_no_title(self):
        response = self.client.post(
            url_for('api.notebooks'),
            headers=self.headers,
            data=json.dumps({
                "bad": "bad"
            }))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response.status_code == 400)
        self.assertEqual(
            'Missing Title of the Notebook', json_response['message']['title'])

    def test_get_single_notebook(self):
        # Will neeed to use headers twice
        local_headers = self.headers

        # Create new Notebook
        self.client.post(
            url_for('api.notebooks'),
            headers=local_headers,
            data=json.dumps({
                "title": "Test Notebook Title"
            }))

        response = self.client.get(
            url_for('api.notebook', notebook_id=1),
            headers=local_headers)

        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            'Test Notebook Title' in response.get_data(as_text=True))

    def test_get_single_notebook_not_owned(self):
        someone_else = self.add_other_user()

        other_nb = Notebook(
            title='Other Title',
            author_id=someone_else.id)

        db.session.add(other_nb)
        db.session.commit()

        response = self.client.get(
            url_for('api.notebook', notebook_id=other_nb.id),
            headers=self.headers)

        self.assertTrue(response.status_code == 404)

    def test_get_single_notebook_not_exist(self):
        response = self.client.get(
            url_for('api.notebook', notebook_id=1000),
            headers=self.headers)

        self.assertTrue(response.status_code == 404)

    def test_update_notebook(self):
        # Will neeed to use headers twice
        local_headers = self.headers

        # Create new Notebook
        self.client.post(
            url_for('api.notebooks'),
            headers=local_headers,
            data=json.dumps({
                "title": "Test Notebook Title"
            }))

        # Update Notebook Title
        response = self.client.put(
            url_for('api.notebook', notebook_id=1),
            headers=local_headers,
            data=json.dumps({
                "title": "Updated Test Notebook Title"
            }))

        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            'Updated Test Notebook Title' in response.get_data(as_text=True))

        # Update Notebook Deleted Status
        response = self.client.put(
            url_for('api.notebook', notebook_id=1),
            headers=local_headers,
            data=json.dumps({
                "is_deleted": True
            }))

        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(json_response['notebook']['is_deleted'])

        # Undo Deletion
        response = self.client.put(
            url_for('api.notebook', notebook_id=1),
            headers=local_headers,
            data=json.dumps({
                "is_deleted": False
            }))

        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 200)
        self.assertFalse(json_response['notebook']['is_deleted'])

    def test_delete_notebook(self):
        # Will neeed to use headers twice
        local_headers = self.headers

        # Create new Notebook
        self.client.post(
            url_for('api.notebooks'),
            headers=local_headers,
            data=json.dumps({
                "title": "Test Notebook Title"
            }))

        # Update Notebook Title
        response = self.client.delete(
            url_for('api.notebook', notebook_id=1),
            headers=local_headers)

        self.assertTrue(response.status_code == 200)
