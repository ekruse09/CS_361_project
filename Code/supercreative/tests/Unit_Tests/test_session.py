from django.test import TestCase, Client
from supercreative.models import (User, UserRole)
from supercreative.authentication.authentication import active_session_exists
from supercreative.user import user


class UnitTestActiveSessionExists(TestCase):
    good_session = None
    bad_session = None
    good_client = None
    bad_client = None
    user = None

    def setUp(self):
        user.create_user("test@uwm.edu",
                         "P@ssword123",
                         UserRole.objects.create(role_name="Administrator").role_name,
                         "John",
                         "Doe",
                         "1234567890",
                         "123 Main St")

        self.user = User.objects.get(email="test@uwm.edu")
        self.good_client = Client()
        self.good_session = self.good_client.session
        self.good_session['user_id'] = self.user.user_id
        self.good_session['role'] = self.user.role_id.role_name
        self.good_session.save()

        self.bad_client = Client()
        self.bad_session = self.bad_client.session

    def test_active_session(self):
        # Assert that session exists and that user role is legitimate
        self.assertTrue(active_session_exists(self.good_client), "No active session")

    def test_no_session(self):
        # Assert that session does not exist
        self.assertFalse(active_session_exists(self.bad_client), "Session should not exist")


class AcceptanceTestActiveSessionExists(TestCase):
    good_session = None
    bad_session = None
    good_client = None
    bad_client = None
    user = None

    def setUp(self):
        user.create_user("test@uwm.edu",
                         "P@ssword123",
                         UserRole.objects.create(role_name="Administrator").role_name,
                         "John",
                         "Doe",
                         "1234567890",
                         "123 Main St")

        self.user = User.objects.get(email="test@uwm.edu")
        self.good_client = Client()
        self.good_session = self.good_client.session
        self.good_session['user_id'] = self.user.user_id
        self.good_session['role'] = self.user.role_id.role_name
        self.good_session.save()

        self.bad_client = Client()
        self.bad_session = self.bad_client.session

    def test_good_session(self):
        # Assert that user stays on page if session is valid
        resp = self.good_client.get("/test/", follow=True)
        self.assertEqual(resp.status_code, 200, "Did not login successfully")

    def test_bad_session(self):
        # Assert that user is redirected if session is invalid
        resp = self.bad_client.get("/test/", follow=True)
        self.assertRedirects(resp, '/', status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
