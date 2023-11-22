import os
import string
from django.test import TestCase
from supercreative.models import User
from supercreative.CreateAccount.CreateAccount import create_user

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")

class CreateAccountTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id=1, email="test@uwm.edu", password="Testp@ss", role="TA",
                                        first_name="testfirst", last_name="testlast", phone_number="5555555555",
                                        address="testaddress")

    def test_badid(self):
        self.assertTrue(isinstance(User.objects.get(user_id=1).user_id, int))
        self.assertEqual(User.objects.get(user_id=1).user_id, 1)
        self.assertNotEqual(User.objects.get(user_id=1).user_id, '')

    def test_existingid(self):
        self.assertFalse(not User.objects.filter(user_id=1).exists())

    def test_bademail(self):
        self.assertTrue(isinstance(User.objects.get(email="test@uwm.edu").email, str))
        self.assertEqual(User.objects.get(email="test@uwm.edu").email, "test@uwm.edu")
        self.assertNotEqual(User.objects.get(email="test@uwm.edu").email, "")
        hold = User.objects.get(user_id=1).email
        if '@' in hold:
            site = hold.partition('@')
            self.assertEqual(site[2], "uwm.edu")
            self.assertNotEqual(site, "")
        else:
            self.fail("Invalid email")

    def test_badpass(self):
        self.assertTrue(isinstance(User.objects.get(password="Testp@ss").password, str))
        self.assertEqual(User.objects.model(password="Testp@ss").password, "Testp@ss")
        self.assertNotEqual(User.objects.model(password="Testp@ss").password, "")
        upper = any(i.isupper() for i in User.objects.get(user_id=1).password)
        lower = any(i.islower() for i in User.objects.get(user_id=1).password)
        special = any(i in string.punctuation for i in User.objects.get(user_id=1).password)
        self.assertTrue(upper)
        self.assertTrue(lower)
        self.assertTrue(special)

    def test_badrolemodel(self):
        self.assertTrue(isinstance(User.objects.get(role="TA").role, str))
        self.assertEqual(User.objects.model(role="TA").role, "TA")
        self.assertNotEqual(User.objects.model(role="TA").role, "")

    def test_badfirst(self):
        self.assertTrue(isinstance(User.objects.get(first_name="testfirst").first_name, str))
        self.assertEqual(User.objects.model(first_name="testfirst").first_name, "testfirst",)
        self.assertNotEqual(User.objects.model(first_name="testfirst").first_name, "",)

    def test_badlast(self):
        self.assertTrue(isinstance(User.objects.get(last_name="testlast").last_name, str))
        self.assertEqual(User.objects.model(last_name="testlast").last_name, "testlast", )
        self.assertNotEqual(User.objects.model(last_name="testlast").last_name, "", )

    def test_badphone(self):
        self.assertTrue(isinstance(User.objects.get(phone_number="5555555555").phone_number, str))
        self.assertEqual(User.objects.model(phone_number="5555555555").phone_number, "5555555555", )
        self.assertNotEqual(User.objects.model(phone_number="5555555555").phone_number, "", )
        self.assertEqual(len(User.objects.get(user_id=1).phone_number), 10)

    def test_badadress(self):
        self.assertTrue(isinstance(User.objects.get(address="testaddress").address, str))
        self.assertEqual(User.objects.model(address="testaddress").address, "testaddress", )
        self.assertNotEqual(User.objects.model(address="testaddress").address, "", )
