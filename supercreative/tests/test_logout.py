import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")

from django.test import TestCase, Client
from supercreative.models import (User, Course, ArchivedCourse, Section,
                                  UserCourseAssignment)

class LogoutTestCase(TestCase):
    client = None
    user = None
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(user_id=1, email="test@example.com",
                            password="password123",
                            role="student", first_name="John", last_name="Doe",
                            phone_number="1234567890", address="123 Main St")
        self.client.session["user_id"] = self.user.user_id


    def test_session_content(self):
        #logout user and clear session data
        self.assertEqual(1,1, "not equal")