from django.test import TestCase, Client
from supercreative.models import (User, Course, Section, UserCourseAssignment)
from supercreative.Logout.logout import logout

class LogoutTestCase(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        self.client = Client()
        self.session = self.client.session
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.session['user_id'] = self.user.user_id
        self.session['role'] = self.user.role
        self.session.save()
        for key, value in self.session.items():
            print(key)

    def test_delete_session_key(self):
        # User is logged in
        self.assertEqual(self.client.session['user_id'], self.session['user_id'])
        logout(self.client.session)
        with self.assertRaises(KeyError):
            print(self.client.session['user_id'])
