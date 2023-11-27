from django.test import TestCase, Client
from supercreative.models import (User, Course, Section)
from supercreative.session.session import active_session_exists

class UnitTestActiveSessionExists(TestCase):
    good_session = None
    bad_session = None
    good_client = None
    bad_client = None
    user = None
    def setUp(self):
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.good_client = Client()
        self.good_session = self.good_client.session
        self.good_session['user_id'] = self.user.user_id
        self.good_session['role'] = self.user.role
        self.good_session.save()

        self.bad_client = Client()
        self.bad_session = self.bad_client.session

    def test_active_session(self):
        # Assert that session exists and that user role is legitimate
        self.assertTrue(active_session_exists(self.good_session), "No active session")

    def test_no_session(self):
        # Assert that session does not exist
        self.assertFalse(active_session_exists(self.bad_session), "Session should not exist")

class AcceptanceTestActiveSessionExists(TestCase):
    good_session = None
    bad_session = None
    good_client = None
    bad_client = None
    user = None

    def setUp(self):
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.good_client = Client()
        self.good_session = self.good_client.session
        self.good_session['user_id'] = self.user.user_id
        self.good_session['role'] = self.user.role
        self.good_session.save()

        self.bad_client = Client()
        self.bad_session = self.bad_client.session

    def test_good_session(self):
        # Assert that user stays on page if session is valid
        resp = self.good_client.get("/test/", follow=True)
        self.assertEqual(resp.status_code,200, "Did not login successfully")



    def test_bad_session(self):
        # Assert that user is redirected if session is invalid
        resp = self.bad_client.get("/test/", follow=True)
        self.assertRedirects(resp, '/', status_code=302, target_status_code=200,
                             fetch_redirect_response=True)