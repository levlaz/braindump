from client_base import ClientTestCase


class AuthViewTestCase(ClientTestCase):

    def test_login_logout(self):
        self.add_user()
        response = self.login('test@example.com', 'password')
        self.assertTrue("Add a Note" in response.get_data(as_text=True))

        response = self.logout()
        self.assertTrue("You have been logged out." in response.get_data(as_text=True))

    def test_login_logged(self):
        u = self.add_user()
        u_last_login = u.last_login_date

        self.login(u.email, 'password')

        u_last_login_updated = u.last_login_date
        self.assertNotEqual(u_last_login, u_last_login_updated)