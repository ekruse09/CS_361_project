import os
from django.test import TestCase
from supercreative.user.user import create_user
from supercreative.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")


class CreateAccountTest(TestCase):
    def test_good_create(self):
        goodcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555","testaddress")
        self.assertTrue(goodcreate)
        self.assertEqual(User.objects.get(user_id=1).user_id, 1)
        self.assertEqual(User.objects.get(user_id=1).email, "test@uwm.edu")
        self.assertEqual(User.objects.get(user_id=1).password, "Testp@ss")
        self.assertEqual(User.objects.get(user_id=1).role, "TA")
        self.assertEqual(User.objects.get(user_id=1).first_name, "testfirst")
        self.assertEqual(User.objects.get(user_id=1).last_name, "testlast")
        self.assertEqual(User.objects.get(user_id=1).phone_number, "5555555555")
        self.assertEqual(User.objects.get(user_id=1).address, "testaddress")

    def test_existing_user(self):
        goodcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "testaddress")
        dupeidcreate = create_user(1, "again@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "testaddress")
        dupemailcreate = create_user(2, "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "testaddress")
        self.assertFalse(dupeidcreate)
        self.assertFalse(dupemailcreate)

    def test_bad_id(self):
        badcreate = create_user(-1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_email(self):
        badcreate = create_user(1, "bademail", "Testp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_pass_L(self):
        badcreate = create_user(1, "test@uwm.edu", "badp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_pass_U(self):
        badcreate = create_user(1, "test@uwm.edu", "BADP@SS", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_pass_S(self):
        badcreate = create_user(1, "test@uwm.edu", "Badpass", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_role(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "norole", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_phone_size(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555555555",
                                 "testaddress")
        self.assertFalse(badcreate)

    def test_bad_phone_hypen(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555-555-5555",
                                 "testaddress")
        self.assertTrue(badcreate)

    def test_bad_phone_parentheses(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "(555)5555555",
                                 "testaddress")
        self.assertTrue(badcreate)

    def test_bad_phone_ws(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555 555 5555",
                                 "testaddress")
        self.assertTrue(badcreate)

    def test_bad_address(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 123)
        self.assertFalse(badcreate)

    def test_no_create(self):
        nonecreate = create_user("", "", "", "", "", "", "", "")
        self.assertFalse(nonecreate)
