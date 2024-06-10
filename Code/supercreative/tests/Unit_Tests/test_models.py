import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")

from django.test import TestCase
from supercreative.models import User, Course, Section, UserCourseAssignment, UserRole, SectionType
from datetime import date
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercreative.settings")


class UserTestCase(TestCase):
    def setUp(self):
        self.role = UserRole.objects.create(role_name="Student")
        self.user = User.objects.create(email="test@example.com",
                                        password="password123",
                                        role_id=self.role,
                                        first_name="John",
                                        last_name="Doe",
                                        phone_number="1234567890",
                                        address="123 Main St")

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.role_id, self.role)


class CourseTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(course_name="Introduction to Python",
                                            course_description="A basic course on Python programming",
                                            course_code="PY101")

    def test_course_creation(self):
        self.assertEqual(self.course.course_name, "Introduction to Python")
        self.assertEqual(self.course.course_code, "PY101")
        self.assertEqual(self.course.course_description, "A basic course on Python programming")


class SectionTestCase(TestCase):
    def setUp(self):
        self.section_type = SectionType.objects.create(section_type_name="Lecture")
        self.course = Course.objects.create(course_name="Data Science with Python",
                                            course_description="Data Science concepts using Python",
                                            course_code="DS101")
        self.section = Section.objects.create(course_id=self.course, section_type=self.section_type)

    def test_section_creation(self):
        self.assertEqual(self.section.section_type, self.section_type)
        self.assertEqual(self.section.course_id.course_name, "Data Science with Python")
        self.assertEqual(self.section.course_id.course_code, "DS101")


class UserCourseAssignmentTestCase(TestCase):
    def setUp(self):
        self.section_type = SectionType.objects.create(section_type_name="Lecture")
        self.role = UserRole.objects.create(role_name="Student")
        self.user = User.objects.create(email="jane@example.com",
                                        password="password456",
                                        role_id=self.role,
                                        first_name="Jane",
                                        last_name="Smith",
                                        phone_number="0987654321",
                                        address="456 Elm St")
        self.course = Course.objects.create(course_name="Web Development",
                                            course_description="Web development basics",
                                            course_code="WD101")
        self.section = Section.objects.create(section_id=2, course_id=self.course, section_type=self.section_type)

    def test_user_course_assignment(self):
        # create a user course assignment with the user, course, and section
        assignment = UserCourseAssignment.objects.create(user_id=self.user,
                                                         section_id=self.section,
                                                         course_id=self.course,
                                                         section_type=self.section_type)
        self.assertEqual(assignment.course_id, self.course, "Course does not match expected value")
        self.assertEqual(assignment.section_type, self.section_type, "SectionType does not match expected value")
        self.assertEqual(assignment.user_id, self.user, "User does not match expected value")


class UserRoleTestCase(TestCase):
    def setUp(self):
        self.role = UserRole.objects.create(role_name="Administrator")

    def test_user_role_creation(self):
        self.assertTrue(UserRole.objects.filter(role_name=self.role.role_name).exists(),
                        "Failed to create new user role.")


class SectionTypeTestCase(TestCase):
    def setUp(self):
        self.section_type = SectionType.objects.create(section_type_name="Lecture")

    def test_section_type_creation(self):
        self.assertTrue(SectionType.objects.filter(section_type_name=self.section_type.section_type_name).exists(),
                        "Failed to create new section type")
