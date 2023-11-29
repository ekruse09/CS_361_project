from django.test import TestCase
from django.urls import reverse
from supercreative.models import Course

class CoursesViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Course.objects.create(course_id='1', course_name='Test Course', course_description='Test Description', course_code='TC101')

    def test_get_courses(self):
        response = self.client.get('/courses/')  # Replace with your actual URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('courses', response.context)
        self.assertTrue(response.context['pool'])

    def test_post_view_course(self):
        response = self.client.post('/courses/', {'action': 'view_course', 'course_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course.html')
        self.assertIn('course', response.context)
        self.assertTrue(response.context['pool'])
        self.assertFalse(response.context['edit'])

    def test_post_request_edit(self):
        response = self.client.post('/courses/', {'action': 'request_edit', 'course_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course.html')
        self.assertIn('course', response.context)
        self.assertTrue(response.context['pool'])
        self.assertTrue(response.context['edit'])

    def test_post_request_new(self):
        response = self.client.post('/courses/', {'action': 'request_new'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course.html')
        self.assertTrue(response.context['pool'])
        self.assertTrue(response.context['edit'])

    def test_post_new_course(self):
        response = self.client.post('/courses/', {'action': 'new_course', 'course_id': '2', 'course_name': 'New Course', 'course_description': 'New Description', 'course_code': 'NC102'})
        self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(Course.objects.count(), 2)

    def test_post_edit_course(self):
        response = self.client.post('/courses/', {'action': 'edit_course', 'course_id': '1', 'course_name': 'Updated Course', 'course_description': 'Updated Description', 'course_code': 'UC103'})
        self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        updated_course = Course.objects.get(course_id='1')
        self.assertEqual(updated_course.course_name, 'Updated Course')

    def test_post_delete_course(self):
        response = self.client.post('/courses/', {'action': 'delete_course', 'course_id': '1'})
        self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(Course.objects.count(), 0)

    def test_post_invalid_action(self):
        response = self.client.post('/courses/', {'action': 'invalid_action'})
        self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
