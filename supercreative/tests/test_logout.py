from django.test import TestCase, Client
from supercreative.models import (User, Course, Section, UserCourseAssignment)
from supercreative.Logout.logout import logout

class LogoutTestCase(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # Session keys would not save if only using self.client.session. Not sure why because self.session and
        # self.client.session are the same object
        self.client = Client()
        self.session = self.client.session
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.session['user_id'] = self.user.user_id
        self.session['role'] = self.user.role
        self.session.save()

    def test_delete_session_key(self):
        # verifies that user_id key does exist
        self.assertEqual(self.user.user_id, self.client.session['user_id'])

        # logs user out by deleting session keys
        logout(self.client.session)

        # verify that session keys have been deleted
        for key, value in self.session.items():
            with self.assertRaises(KeyError):
                self.client.session[key]
