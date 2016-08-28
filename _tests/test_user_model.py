import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='password')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='password')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='password')
        self.assertTrue(u.verify_password('password'))
        self.assertFalse(u.verify_password('password2'))

    def test_password_salts_are_random(self):
        u = User(password='password')
        u2 = User(password='password')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_confirmation(self):
        u = User(password='password')
        confirmation_token = u.generate_confirmation_token()
        u.confirm(confirmation_token)
        self.assertTrue(u.confirmed)

    def test_password_reset(self):
        u = User(password='password')
        old_password_hash = u.password_hash
        reset_token = u.generate_reset_token()
        u.reset_password(reset_token, 'new_password')
        self.assertTrue(u.password_hash != old_password_hash)
