import os

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
        emails = []
        self.assertEqual(user.getEmails(), emails)
        emails.append("test@gmail.com")
        user.addEmail("test@gmail.com")
        emails.append("test2@gmail.com")
        user.addEmail("test2@gmail.com")
        self.assertEqual(user.getEmails(), emails)
        emails.remove("test2@gmail.com")
        user.removeEmail("test2@gmail.com")
        self.assertEqual(user.getEmails(), emails)
        user.clearEmails()
        self.assertEqual(user.getEmails(), [])



