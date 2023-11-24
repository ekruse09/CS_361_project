import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")

from django.test import TestCase, Client
from supercreative.models import (User, Course, Section)

class TestLogin(TestCase):
    def setUp(self):
        # same user setup as everyone else used
        self.client = Client()
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.client.session["user_id"] = self.user.user_id

    # tests assume we login with email and password
    def test_wrongPassword(self):
        # modeled after TestSessionLab2's test_wrongPassword
        resp = self.client.post("/", {"email": "wrong@email.com", "password": "wrong"}, follow=True)
        self.assertEqual(resp.context["message"], "Invalid email address or password.", "user logged in with bad "
                                                                                        "password")

    def test_noPassword(self):
        # modeled after TestSessionLab2's test_wrongPassword
        resp = self.client.post("/", {"email": "wrong@email.com", "password": ""}, follow=True)
        self.assertEqual(resp.context["message"], "Invalid email address or password.", "user logged in with no "
                                                                                        "password")

    def test_session(self):
        # assumes the session is named after the user_id
        resp = self.client.post("/", {"email": "test@example.com", "password": "password123"}, follow=True)
        self.assertEqual(self.client.session["user_id"], "1", "incorrect session!")

    def test_complete(self):
        # tests to see if the complete list of user's data is correct
        resp = self.client.post("/", {"email": "test@example.com", "password": "password123"}, follow=True)

        self.assertEqual(self.client.session["email"], "test@example.com", "incorrect email!")
        self.assertEqual(self.client.session["password"], "password123", "incorrect password!")
        self.assertEqual(self.client.session["role"], "student", "incorrect role!")
        self.assertEqual(self.client.session["first_name"], "John", "incorrect first name!")
        self.assertEqual(self.client.session["last_name"], "Doe", "incorrect last name!")
        self.assertEqual(self.client.session["phone_number"], "1234567890", "incorrect phone number!")
        self.assertEqual(self.client.session["address"], "123 Main St", "incorrect address!")


    '''
    def test_runtests(self):
        #do my tests run
        self.assertEqual(1,1, "not equal")
    '''