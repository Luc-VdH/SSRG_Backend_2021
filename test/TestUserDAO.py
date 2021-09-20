import os

from src.UserDAO import UserDAO
import unittest


class TestUserDAO(unittest.TestCase):
    def test_user(self):
        ud = UserDAO()
        ud.addUser("daotest", "password", "mossid")
        self.assertEqual(ud.userExists("daotest"), True)
        login = ud.signIn("daotest", "password")
        self.assertEqual(login, 1)
        self.assertEqual(ud.getUserMossid("daotest"), "mossid")

        ud.addUserEmail("daotest", "test@123.com")
        self.assertEqual(ud.getUserEmail("daotest"), ["test@123.com"])

        ud.removeUserEmail("daotest", "test@123.com")
        self.assertEqual(ud.getUserEmail("daotest"), [])

        ud.updateUserInfo("daotest", "password2", "mossid2")
        login = ud.signIn("daotest", "password2")
        self.assertEqual(login, 1)
        self.assertEqual(ud.getUserMossid("daotest"), "mossid2")

        ud.deleteUser("daotest", "password2")
        self.assertEqual(ud.userExists("daotest"), False)

