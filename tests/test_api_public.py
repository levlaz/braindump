import json
from flask import url_for
from api_base import ApiBaseTestCase


class PublicApiTestCase(ApiBaseTestCase):

    def test_public_stats_empty(self):

        res = self.client.get('/api/v1/public/stats')

        json_res = json.loads(res.data.decode('utf-8'))

        self.assertEqual(0, json_res['users'])
        self.assertEqual(0, json_res['notes'])

    def test_public_stats_with_user(self):

        self.add_user()
        self.add_other_user()

        res = self.client.get('/api/v1/public/stats')

        json_res = json.loads(res.data.decode('utf-8'))

        self.assertEqual(2, json_res['users'])

    def test_public_states_with_notes(self):

        u = self.add_user()
        nb = self.add_notebook(u)
        note = self.add_note(nb, u)

        res = self.client.get('/api/v1/public/stats')

        json_res = json.loads(res.data.decode('utf-8'))

        self.assertEqual(1, json_res['users'])
        self.assertEqual(1, json_res['notes'])

        u1n2 = self.add_note(nb, u)
        u1n3 = self.add_note(nb, u)

        u2 = self.add_other_user()
        nb2 = self.add_notebook(u2)
        note = self.add_note(nb2, u2)

        res = self.client.get('/api/v1/public/stats')

        json_res = json.loads(res.data.decode('utf-8'))

        self.assertEqual(2, json_res['users'])
        self.assertEqual(4, json_res['notes'])