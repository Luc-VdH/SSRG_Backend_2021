import os

from src.Email import Email
import unittest

#unittest class to test the Job Class
class test_email(unittest.TestCase):
    #unittest for the correct behavior of sending an email
    def test_send(self):
        email = Email(["cscmailaddress+test_class@gmail.com"], "test_email")
        output = email.send()
        self.assertEqual(output, True)
