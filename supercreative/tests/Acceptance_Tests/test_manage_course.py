from django.test import TestCase, Client
from supercreative.models import Course, UserCourseAssignment, Section
from supercreative.course import course
from supercreative.user import user
from supercreative.authentication import authentication


class ManageCourseAcceptanceTests(TestCase):
    client = None
    course = None
    user = None
    section1 = None
    section2 = None

    def setUp(self):
        self.client = Client()

        # Set up data for the whole TestCase
        self.course = course.create_course(1, 'Test Course', 'Test Description', 'TC101')
        self.user = user.create_user(1, 'test@uwm.edu', 'P@ssword123', 'ADMINISTRATOR', 'Jayson',
                                     'Rock', '1234567890', '123 Sesame St')

        section1 = Section.objects.create(course=self.course, section_id=1, section_type='Lab')
        section2 = Section.objects.create(course=self.course, section_id=2, section_type='Lecture')

        authentication.create_session(self.client.session, 'test@uwm.edu')
