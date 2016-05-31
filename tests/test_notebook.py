import unittest

from flask import url_for
from flask_login import current_user
from app import create_app, db
from app.models import User, Notebook


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

    def login_as_admin(self):
        u = User.query.filter_by(email='admin@email.com').first()

        response = self.client.post(url_for('auth.login'), data={
          'email': 'admin@email.com',
          'password': 'admin'
        }, follow_redirects=True)

    def test_creating_notebook(self):
        self.login_as_admin()

        # Create a New Notebook
        n = Notebook(title="New Notebook", author_id=1)
        db.session.add(n)
        db.session.commit()

        # Verify that the New Notebook Exists
        user = User.query.filter_by(id=1).first_or_404()
        self.assertTrue('New Notebook' in user.notebooks[0].title)

        # Verify that the new Notebook link is correct
        response = self.client.get(url_for('main.notebook', id=n.id))
        self.assertTrue('Notes in New Notebook' in response.get_data(as_text=True))
