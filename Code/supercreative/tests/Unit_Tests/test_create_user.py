import os
from django.test import TestCase
from supercreative.user.user import create_user
from supercreative.models import User, UserRole

class CreateAccountTest(TestCase):
    def setUp(self):
        self.role = UserRole.objects.create(role_name="TA")
    def test_good_create(self):
        result = create_user("test@uwm.edu", "Testp@ss", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "User created successfully.")
        user = User.objects.get(email="test@uwm.edu")
        self.assertEqual(user.email, "test@uwm.edu")
        self.assertEqual(user.password, "Testp@ss")
        self.assertEqual(user.role_id.role_name, "TA")
        self.assertEqual(user.first_name, "testfirst")
        self.assertEqual(user.last_name, "testlast")
        self.assertEqual(user.phone_number, "5555555555")
        self.assertEqual(user.address, "testaddress")

    def test_existing_user(self):
        create_user("test@uwm.edu", "Testp@ss", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        result = create_user("test@uwm.edu", "Testp@ss", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Email already exists.", "Allowed duplicate email.")

    def test_bad_email(self):
        result = create_user("bademail", "Testp@ss", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "email must contain an @ symbol.")

    def test_bad_pass_L(self):
        result = create_user("test@uwm.edu", "badp@ss", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")

    def test_bad_pass_U(self):
        result = create_user("test@uwm.edu", "BADP@SS", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")

    def test_bad_pass_S(self):
        result = create_user("test@uwm.edu", "Badpass", self.role.role_name, "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Password must contain at least one uppercase letter, one lowercase letter, and one special character.")

    def test_bad_role(self):
        result = create_user("test@uwm.edu", "Testp@ss", "norole", "testfirst", "testlast", "5555555555", "testaddress")
        self.assertEqual(result, "Invalid role selected.")

    def test_bad_phone_size(self):
        result = create_user("test@uwm.edu", "Testp@ss", self.role.role_name, "testfirst", "testlast", "555555555", "testaddress")
        self.assertEqual(result, "Phone number must be 10 digits.")

    def test_bad_address(self):
        result = create_user("test@uwm.edu", "Testp@ss", self.role.role_name, "testfirst", "testlast", "5555555555", 123)
        self.assertEqual(result, "Address must be a string and non-empty.")


