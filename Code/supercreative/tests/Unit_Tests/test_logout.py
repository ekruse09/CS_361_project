from django.test import TestCase, Client
from supercreative.models import User, UserRole
from supercreative.authentication.authentication import end_session
from supercreative.user.user import create_user
from supercreative.authentication.authentication import create_session


class LogoutUnitTest(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # Session keys would not save if only using self.client.session. Not sure why because self.session and
        # self.client.session are the same object
        user = User.objects.get
        self.client = Client()
        self.session = self.client.session
        create_user("test@uwm.edu", "P@ssword123", UserRole.objects.create(role_name="Administrator").role_name, "John", "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(email="test@uwm.edu")
        create_session(self.session, self.user.email)

    def test_delete_session_key(self):
        # verifies that user_id key does exist
        self.assertEqual(self.user.user_id, self.client.session['user_id'])

        # logs user out by deleting session keys
        end_session(self.client.session)

        # verify that session keys have been deleted
        for key, value in self.session.items():
            with self.assertRaises(KeyError):
                self.client.session[key]
