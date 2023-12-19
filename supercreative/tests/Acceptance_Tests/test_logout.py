from django.test import TestCase, Client
from supercreative.models import User, UserRole
from supercreative.user.user import create_user
from supercreative.authentication.authentication import create_session


class LogoutAcceptanceTest(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # Session keys would not save if only using self.client.session. Not sure why because self.session and
        # self.client.session are the same object
        self.client = Client()
        self.session = self.client.session
        create_user("test@uwm.edu", "P@ssword123", UserRole.objects.create(role_name="Administrator").role_name, "John", "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(email="test@uwm.edu")
        create_session(self.session, self.user.email)

    def test_acceptance_end_session(self):
        # assert that session exists
        self.assertEqual(self.client.session['user_id'], self.user.user_id)

        # redirect to login simulates user clicking logout link
        self.client.get('/', follow=True)

        # assert that session has been cleared
        for key, value in self.session.items():
            with self.assertRaises(KeyError):
                self.client.session[key]
