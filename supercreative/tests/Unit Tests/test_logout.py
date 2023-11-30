from django.test import TestCase, Client
from supercreative.models import User
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
        create_user(1, "test@uwm.edu", "P@ssword123", "ADMINISTRATOR", "John", "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(user_id=1)
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


class LogoutAcceptanceTest(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # Session keys would not save if only using self.client.session. Not sure why because self.session and
        # self.client.session are the same object
        user = User.objects.get
        self.client = Client()
        self.session = self.client.session
        create_user(1, "test@uwm.edu", "P@ssword123", "ADMINISTRATOR", "John", "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(user_id=1)
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
