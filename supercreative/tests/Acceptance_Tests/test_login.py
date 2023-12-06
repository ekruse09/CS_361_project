from django.test import TestCase, Client
from supercreative.user import user
from supercreative.models import User


class LoginAcceptanceTest(TestCase):
    client = None
    user = None
    session = None

    def setUp(self):
        # same user setup as everyone else used
        self.client = Client()
        user.create_user(1, "test@uwm.edu", "P@ssword123", "ADMINISTRATOR", "John", "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(user_id=1)
        self.session = self.client.session

    def test_successful_login(self):
        resp = self.client.post("/", {'email': self.user.email, 'password': self.user.password}, follow=True)
        self.assertRedirects(resp, "home/", status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        self.assertEqual(resp.context['user_id'], self.user.user_id, "Emails do not match")

    def test_invalid_email(self):
        resp = self.client.post("/", {'email': "email@bad.com", 'password': self.user.password}, follow=True)
        self.assertEqual(resp.context['message'], "No account found with that email and password",
                         "Invalid email should return error message")

    def test_invalid_password(self):
        resp = self.client.post("/", {'email': self.user.email, 'password': 'badpassword'}, follow=True)
        self.assertEqual(resp.context['message'], "No account found with that email and password",
                         "Invalid password should return error message")