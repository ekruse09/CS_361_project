import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")

from django.test import TestCase
from supercreative.models import User, Course, Section, UserCourseAssignment
from datetime import date

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(user_id=1, email="test@example.com", password="password123",
                            role="student", first_name="John", last_name="Doe",
                            phone_number="1234567890", address="123 Main St")

    def test_user_creation(self):
        user = User.objects.get(user_id=1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, "student")

class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(course_id=101, course_name="Introduction to Python",
                              course_description="A basic course on Python programming",
                              course_code="PY101")

    def test_course_creation(self):
        course = Course.objects.get(course_id=101)
        self.assertEqual(course.course_name, "Introduction to Python")
        self.assertEqual(course.course_code, "PY101")
        self.assertEqual(course.course_description, "A basic course on Python programming")

class SectionTestCase(TestCase):
    def setUp(self):
        course = Course.objects.create(course_id=103, course_name="Data Science with Python",
                                       course_description="Data Science concepts using Python",
                                       course_code="DS101")
        Section.objects.create(section_id=1, course_id=course, section_type="Lecture")
        print(UserCourseAssignment.objects.all())

    def test_section_creation(self):
        section = Section.objects.get(section_id=1)
        self.assertEqual(section.section_type, "Lecture")
        self.assertEqual(section.course_id.course_name, "Data Science with Python")
        self.assertEqual(section.course_id.course_code, "DS101")

class UserCourseAssignmentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id=2, email="jane@example.com", password="password456",
                                   role="student", first_name="Jane", last_name="Smith",
                                   phone_number="0987654321", address="456 Elm St")
        self.course = Course.objects.create(course_id=104, course_name="Web Development",
                                       course_description="Web development basics",
                                       course_code="WD101")
        self.section = Section.objects.create(section_id=2, course_id=self.course, section_type="Online")

    def test_user_course_assignment(self):
        #create a user course assignment with the user, course, and section
        assignment = UserCourseAssignment.objects.create(user_id=self.user, section_id=self.section, course_id=self.course, section_type="Online")
        self.assertEqual(assignment.course_id.course_name, "Web Development")
        self.assertEqual(assignment.section_type, "Online")
        self.assertEqual(assignment.user_id.first_name, "Jane")

