import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")

from django.test import TestCase
from supercreative.models import User, Course, ArchivedCourse, Section, UserCourseAssignment
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

class ArchivedCourseTestCase(TestCase):
    def setUp(self):
        course = Course.objects.create(course_id=102, course_name="Advanced Python",
                                       course_description="An advanced course on Python programming",
                                       course_code="PY201")
        ArchivedCourse.objects.create(course_id=course.course_id,
                                      course_name=course.course_name,
                                      course_description=course.course_description,
                                      course_code=course.course_code,
                                      archiving_date=date.today())

    def test_archived_course_creation(self):
        archived_course = ArchivedCourse.objects.get(course_id=102)
        self.assertEqual(archived_course.course_name, "Advanced Python")

class SectionTestCase(TestCase):
    def setUp(self):
        course = Course.objects.create(course_id=103, course_name="Data Science with Python",
                                       course_description="Data Science concepts using Python",
                                       course_code="DS101")
        Section.objects.create(section_id=1, course_id=course, section_type="Lecture")

    def test_section_creation(self):
        section = Section.objects.get(section_id=1)
        self.assertEqual(section.section_type, "Lecture")

class UserCourseAssignmentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(user_id=2, email="jane@example.com", password="password456",
                                   role="student", first_name="Jane", last_name="Smith",
                                   phone_number="0987654321", address="456 Elm St")
        course = Course.objects.create(course_id=104, course_name="Web Development",
                                       course_description="Web development basics",
                                       course_code="WD101")
        section = Section.objects.create(section_id=2, course_id=course, section_type="Online")
        UserCourseAssignment.objects.create(user_id=user, section_id=section, course_id=course, section_type="Online")

    def test_user_course_assignment(self):
        assignment = UserCourseAssignment.objects.get(user_id=2)
        self.assertEqual(assignment.course_id.course_name, "Web Development")
        self.assertEqual(assignment.section_type, "Online")
