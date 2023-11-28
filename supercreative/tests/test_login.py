from django.test import TestCase, Client
from supercreative.models import (User)
from supercreative.authentication.authentication import create_session


class LoginUnitTest(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # same user setup as everyone else used
        self.client = Client()
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.session = self.client.session

        for key, value in self.session.items():
            with self.assertRaises(KeyError):
                self.client.session[key]

    # we log in with email and password
    def test_wrong_email(self):
        self.assertFalse(create_session(self.session, "wrong@email.com"))

    def test_session(self):
        # assumes the session is named after the user_id
        self.assertTrue(create_session(self.session, self.user.email))

    def test_complete(self):
        # tests to see if the complete list of user's data is correct
        create_session(self.session, self.user.email)
        self.assertEqual(self.client.session["user_id"], 1, "incorrect session!")
        self.assertEqual(self.client.session["role"], "student", "incorrect role!")
        '''
        not stored in the session but can be added
        
        self.assertEqual(self.client.session["email"], "test@example.com", "incorrect email!")
        self.assertEqual(self.client.session["password"], "password123", "incorrect password!")
        self.assertEqual(self.client.session["first_name"], "John", "incorrect first name!")
        self.assertEqual(self.client.session["last_name"], "Doe", "incorrect last name!")
        self.assertEqual(self.client.session["phone_number"], "1234567890", "incorrect phone number!")
        self.assertEqual(self.client.session["address"], "123 Main St", "incorrect address!")
        '''

class LoginAcceptanceTest(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # same user setup as everyone else used
        self.client = Client()
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.session = self.client.session

    def test_successful_login(self):
        resp = self.client.post("/", {'email':self.user.email, 'password':self.user.password}, follow=True)
        self.assertRedirects(resp, "test/", status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        self.assertEqual(resp.context['user_id'], self.user.user_id, "Emails do not match")
    def test_invalid_email(self):
        resp = self.client.post("/", {'email':"email@bad.com", 'password':self.user.password}, follow=True)
        self.assertEqual(resp.context['message'], "No account found with that email and password",
                         "Invalid email should return error message")

    def test_invalid_password(self):
        resp = self.client.post("/", {'email': self.user.email, 'password': 'badpassword'}, follow=True)
        self.assertEqual(resp.context['message'], "No account found with that email and password",
                         "Invalid password should return error message")
