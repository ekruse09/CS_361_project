from django.test import TestCase, Client
from supercreative.models import Course
from supercreative.course import course
from supercreative.authentication import authentication
from supercreative.user import user


class CourseAcceptanceTests(TestCase):
    client = None
    existing_course = None
    user = None

    def setUp(self):
        self.client = Client()

        # Set up data for the whole TestCase
        course.create_course(1, 'Test Course', 'Test Description', 'TC101')
        self.existing_course = Course.objects.get(course_id=1)
        self.user = user.create_user(1, 'test@uwm.edu', 'P@ssword123', 'ADMINISTRATOR', 'Jayson',
                                     'Rock', '1234567890', '123 Sesame St')
        authentication.create_session(self.client.session, 'test@uwm.edu')

    def test_get_courses(self):
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('courses', response.context)

    def test_post_view_course(self):
        response = self.client.post('/course/', {'action': 'view_course', 'course_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('course', response.context)
        self.assertTrue(response.context['popup'])
        self.assertFalse(response.context['edit'])

    def test_post_request_edit(self):
        response = self.client.post('/course/', {'action': 'request_edit', 'course_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertIn('course', response.context)
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])

    def test_post_request_new(self):
        response = self.client.post('/course/', {'action': 'request_new'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses.html')
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])

    def test_post_new_course(self):
        response = self.client.post('/course/', {'action': 'new_course',
                                                 'course_id': '2', 'course_name': 'New Course',
                                                 'course_description': 'New Description',
                                                 'course_code': 'NC102'})

        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
        self.assertEqual(Course.objects.count(), 2)

    def test_post_edit_course(self):
        response = self.client.post('/course/', {'action': 'edit_course',
                                                 'course_id': '1', 'course_name': 'Updated Course',
                                                 'course_description': 'Updated Description',
                                                 'course_code': 'UC103'})

        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
        updated_course = Course.objects.get(course_id='1')
        self.assertEqual(updated_course.course_name, 'Updated Course')

    def test_post_delete_course(self):
        response = self.client.post('/course/', {'action': 'delete_course', 'course_id': '1'})
        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
        self.assertEqual(Course.objects.count(), 0)

    def test_post_invalid_action(self):
        response = self.client.post('/course/', {'action': 'invalid_action'})
        # self.assertRedirects(response, '/course/', status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 200, "Bad response")
