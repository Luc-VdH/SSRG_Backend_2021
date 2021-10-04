import os

from src.Email import Email
import unittest


class test_email(unittest.TestCase):
    def test_send(self):
        email = Email(["cscmailaddress+test_class@gmail.com"], "test_email")
        output = email.send()
        self.assertEqual(output, True)
