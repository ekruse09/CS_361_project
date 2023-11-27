from django.test import TestCase, Client
from django.urls import reverse
from supercreative.models import Course


class CourseViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        # Set up any initial data here, like creating a test course

    def test_create_course(self):
        response = self.client.post(reverse('course/'), {
            'action': 'new_user',
            'course_id': '1',
            'course_name': 'Test Course',
            'course_description': 'Description',
            'course_code': 'TC101'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Course.objects.filter(course_id='1').exists())

    def test_edit_course(self):
        # Assuming a course with course_id '1' already exists
        response = self.client.post(reverse('course/'), {
            'action': 'edit_user',
            'course_id': '1',
            'course_name': 'Updated Course',
            'course_description': 'Updated Description',
            'course_code': 'TC102'
        })
        self.assertEqual(response.status_code, 302)
        updated_course = Course.objects.get(course_id='1')
        self.assertEqual(updated_course.course_name, 'Updated Course')
        # Add more assertions as needed to verify the fields are updated correctly

    def test_delete_course(self):
        # Assuming a course with course_id '1' exists
        response = self.client.post(reverse('course/'), {
            'action': 'delete_user',
            'course_id': '1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Course.objects.filter(course_id='1').exists())

    def test_invalid_action(self):
        response = self.client.post(reverse('course/'), {
            'action': 'invalid_action',
            'course_id': '1'
        })
        self.assertEqual(response.status_code, 302)
