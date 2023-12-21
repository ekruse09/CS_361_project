from django.test import TestCase, Client
from django.urls import reverse
from supercreative.models import User, UserRole
from supercreative.user import user
from supercreative.views import UserPage
from supercreative.authentication import authentication

class UserPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Set up data for the whole TestCase
        self.user_role = UserRole.objects.create(role_name="Administrator")
        self.assertTrue(UserRole.objects.filter(role_name=self.user_role.role_name).exists(), "Failed to create role.")
        user.create_user("test@uwm.edu", "P@ssword123", self.user_role.role_name, "John", "Doe", "1234567890", "123 Main St")
        self.existing_user = User.objects.get(email="test@uwm.edu")
        authentication.create_session(self.client.session, self.existing_user.email)
        self.url = '/user_page/'

    def test_post_with_valid_data(self):
        post_data = {
            'user_id': self.existing_user.user_id,
            'password': 'new_password',
            'role': 'new_role',
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'phone_number': 'new_phone_number',
            'address': 'new_address',
            'skills': 'new_skills'
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)

    def test_post_with_invalid_data(self):
        post_data = {
            'user_id': self.existing_user.user_id,
            'password': 'new_password',
            'role': 'new_role',
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'phone_number': 'new_phone_number',
            'address': 'new_address',
            'skills': 'new_skills'
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
