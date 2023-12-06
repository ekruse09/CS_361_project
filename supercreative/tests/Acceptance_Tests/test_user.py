from django.test import TestCase, Client
from supercreative.models import User
from supercreative.user import user
from supercreative.authentication import authentication


class UserAcceptanceTests(TestCase):
    client = None
    existing_user = None

    def setUp(self):
        self.client = Client()
        # Set up data for the whole TestCase
        user.create_user(1, "test@uwm.edu", "P@ssword123", "ADMINISTRATOR", "John", "Doe",
                         "1234567890", "123 Main St")
        self.existing_user = User.objects.get(user_id=1)
        authentication.create_session(self.client.session, 'test@uwm.edu')

    def test_get_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')
        self.assertIn('users', response.context)

    def test_post_view_course(self):
        response = self.client.post('/users/', {'action': 'view_user', 'user_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')
        self.assertIn('user', response.context)
        self.assertTrue(response.context['popup'])
        self.assertFalse(response.context['edit'])

    def test_post_request_edit(self):
        response = self.client.post('/users/', {'action': 'request_edit', 'user_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')
        self.assertIn('user', response.context)
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])

    def test_post_request_new(self):
        response = self.client.post('/users/', {'action': 'request_new'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])

    def test_post_new_user(self):
        response = self.client.post('/users/', {'action': 'new_user',
                                                'user_id': '2', 'password': 'P@ssword123', 'email': 'jane@uwm.edu',
                                                'role': 'ADMINISTRATOR', 'first_name': 'Jane', 'last_name': 'Smith',
                                                'phone_number': '0987654321', 'address': '456 Sesame St'})

        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
        self.assertEqual(User.objects.count(), 2)

    def test_post_edit_user(self):
        response = self.client.post('/users/', {'action': 'edit_user',
                                                'user_id': 1, 'password': 'P@ssword123', 'role': 'INSTRUCTOR',
                                                'first_name': 'Jayson', 'last_name': 'Rock',
                                                'phone_number': '0987654321',
                                                'address': '456 Sesame St'})

        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
        updated_user = User.objects.get(user_id='1')
        self.assertEqual(updated_user.first_name, 'Jayson')

    def test_post_delete_user(self):
        response = self.client.post('/users/', {'action': 'delete_user', 'user_id': 1})
        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
        self.assertEqual(User.objects.count(), 0)

    def test_post_invalid_action(self):
        response = self.client.post('/users/', {'action': 'invalid_action'})
        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
