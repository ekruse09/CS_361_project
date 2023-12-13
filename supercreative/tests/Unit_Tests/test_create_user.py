import os
from django.test import TestCase
from supercreative.user.user import create_user
from supercreative.models import User

class CreateAccountTest(TestCase):
    def test_good_create(self):
        result = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "User created successfully.")
        user = User.objects.get(user_id=1)
        self.assertEqual(user.email, "test@uwm.edu")
        self.assertEqual(user.password, "Testp@ss")
        self.assertEqual(user.role, "TA")
        self.assertEqual(user.first_name, "testfirst")
        self.assertEqual(user.last_name, "testlast")
        self.assertEqual(user.phone_number, "5555555555")
        self.assertEqual(user.address, "testaddress")

    def test_existing_user(self):
        create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        result = create_user(1, "again@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "User ID already exists.")
        result = create_user(2, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Email must be a unique string.")

    def test_bad_id(self):
        result = create_user(-1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "User ID must be a positive integer.")

    def test_bad_email(self):
        result = create_user(1, "bademail", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "email must contain an @ symbol.")

    def test_bad_pass_L(self):
        result = create_user(1, "test@uwm.edu", "badp@ss", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")

    def test_bad_pass_U(self):
        result = create_user(1, "test@uwm.edu", "BADP@SS", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")

    def test_bad_pass_S(self):
        result = create_user(1, "test@uwm.edu", "Badpass", "TA", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")

    def test_bad_role(self):
        result = create_user(1, "test@uwm.edu", "Testp@ss", "norole", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Role must be one of the following: ADMINISTRATOR, INSTRUCTOR, TA.")

    def test_bad_phone_size(self):
        result = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555555555", "testaddress")
        self.assertEqual(result, "Phone number must be 10 digits.")

    def test_bad_address(self):
        result = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555", 123)
        self.assertEqual(result, "Address must be a string and non-empty.")


