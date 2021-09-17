from src.User import User
import unittest


class TestUser(unittest.TestCase):
    def test_password(self):
        user = User("username", "password", "mossid")
        self.assertEqual(user.getPassword(), "password")
        user.setPassword("newpassword")
        self.assertEqual(user.getPassword(), "newpassword")

    def test_mossid(self):
        user = User("username", "password", "mossid")
        self.assertEqual(user.getMossid(), "mossid")
        user.setMossid("newmossid")
        self.assertEqual(user.getMossid(), "newmossid")

    def test_username(self):
        user = User("username", "password", "mossid")
        self.assertEqual(user.getCoursecode(), "username")

    def test_emails(self):
        user = User("username", "password", "mossid")

