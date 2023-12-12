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
        self.assertEqual(User.objects.get(user_id=1).user_id, 1,"failed id")
        self.assertEqual(User.objects.get(user_id=1).email, "test@uwm.edu","failed email")
        self.assertEqual(User.objects.get(user_id=1).password, "Testp@ss","failed password")
        self.assertEqual(User.objects.get(user_id=1).role, "TA","Failed role")
        self.assertEqual(User.objects.get(user_id=1).first_name, "testfirst","Failed first")
        self.assertEqual(User.objects.get(user_id=1).last_name, "testlast","Failed last")
        self.assertEqual(User.objects.get(user_id=1).phone_number, "5555555555","Failed phone")
        self.assertEqual(User.objects.get(user_id=1).address, "testaddress","Failed address")

    def test_existing_user(self):
        goodcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "testaddress")
        dupeidcreate = create_user(1, "again@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "testaddress")
        dupemailcreate = create_user(2, "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "testaddress")
        self.assertFalse(dupeidcreate,"created dupe id")
        self.assertFalse(dupemailcreate,"created dupe email")

    def test_bad_id(self):
        badcreate = create_user(-1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"created bad id")

    def test_bad_email(self):
        badcreate = create_user(1, "bademail", "Testp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"created bad email")

    def test_bad_pass_U(self):
        badcreate = create_user(1, "test@uwm.edu", "badp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"created bad pass upper")

    def test_bad_pass_L(self):
        badcreate = create_user(1, "test@uwm.edu", "BADP@SS", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"created bad pass lower")

    def test_bad_pass_S(self):
        badcreate = create_user(1, "test@uwm.edu", "Badpass", "TA", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"Created bad pass special")

    def test_bad_role(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "norole", "testfirst", "testlast", "5555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"Created bad role")

    def test_bad_phone_size(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555555555",
                                 "testaddress")
        self.assertFalse(badcreate,"Create bad phone size")

    def test_bad_phone_hypen(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555-555-5555",
                                 "testaddress")
        self.assertTrue(badcreate,"Created bad phone hypen")

    def test_bad_phone_parentheses(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "(555)5555555",
                                 "testaddress")
        self.assertTrue(badcreate,"Created bad phone parentheses")

    def test_bad_phone_ws(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "555 555 5555",
                                 "testaddress")
        self.assertTrue(badcreate,"Created bad phone whitespace")

    def test_bad_address(self):
        badcreate = create_user(1, "test@uwm.edu", "Testp@ss", "TA", "testfirst", "testlast", "5555555555",
                                 123)
        self.assertFalse(badcreate,"Created bad address")

    def test_no_create(self):
        nonecreate = create_user("", "", "", "", "", "", "", "")
        self.assertFalse(nonecreate)
        noidcreate = create_user("", "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "123")
        self.assertFalse(noidcreate, "Failed created no id")
        noemailcreate = create_user(1, "", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "123")
        self.assertFalse(noemailcreate, "Failed created no email")
        nopasscreate = create_user(1, "test@uwm.edu", "", "TA", "testfirst",
                                 "testlast", "5555555555", "123")
        self.assertFalse(nopasscreate, "Failed created no password")
        norolecreate = create_user("", "test@uwm.edu", "Testp@ss", "", "testfirst",
                                 "testlast", "5555555555", "123")
        self.assertFalse(norolecreate, "Failed created no role")
        nofirstcreate = create_user("", "test@uwm.edu", "Testp@ss", "TA", "",
                                 "testlast", "5555555555", "123")
        self.assertFalse(nofirstcreate, "Failed created no firstname")
        nolastcreate = create_user("", "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "", "5555555555", "123")
        self.assertFalse(nolastcreate, "Failed created no lastname")
        nophonecreate = create_user("", "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "", "123")
        self.assertFalse(nophonecreate, "Failed created no phone")
        noaddresscreate = create_user("", "test@uwm.edu", "Testp@ss", "TA", "testfirst",
                                 "testlast", "5555555555", "")
        self.assertFalse(noaddresscreate, "Failed created no address")
