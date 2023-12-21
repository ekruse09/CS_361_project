from django.test import TestCase
from supercreative.models import Course, User, Section, UserCourseAssignment, UserRole, SectionType
from supercreative.course.user_assignments import remove_user_from

class TestRemoveUserFrom(TestCase):
    user = None
    course = None
    course_assignment = None
    section = None
    section_assignment = None

    def setUp(self):
        self.user = User.objects.create(email="test@example.com",
                                        password="password123",
                                        role_id=UserRole.objects.create(role_name="Instructor"),
                                        first_name="John",
                                        last_name="Doe",
                                        phone_number="1234567890",
                                        address="123 Main St")
        self.course = Course.objects.create(course_name="Introduction to Python",
                                            course_description="A basic course on Python programming",
                                            course_code="PY101")
        self.section = Section.objects.create(course_id=self.course,
                                              section_type=SectionType.objects.create(section_type_name="Lecture"))
        self.course_assignment = UserCourseAssignment.objects.create(course_id=self.course,
                                                                     user_id=self.user)
        self.section_assignment = UserCourseAssignment.objects.create(course_id=self.course,
                                                                      user_id=self.user,
                                                                      section_id=self.section)

    def test_remove_user_from_course(self):
        self.assertEqual("User successfully removed from this course.", remove_user_from(self.user, self.course))
        self.assertFalse(UserCourseAssignment.objects.filter(course_id=self.course, user_id=self.user).exists(),
                         "Assignments exist for removed user in this course")


class TestBadRemoveUserFrom(TestCase):
    user = None
    course = None
    course_assignment = None
    section = None
    section_assignment = None

    def setUp(self):
        self.user = User.objects.create(email="test@example.com",
                                        password="password123",
                                        role_id=UserRole.objects.create(role_name="Instructor"),
                                        first_name="John",
                                        last_name="Doe",
                                        phone_number="1234567890",
                                        address="123 Main St")
        self.course = Course.objects.create(course_name="Introduction to Python",
                                            course_description="A basic course on Python programming",
                                            course_code="PY101")
        self.section = Section.objects.create(course_id=self.course,
                                              section_type=SectionType.objects.create(section_type_name="Lecture"))
        self.course_assignment = UserCourseAssignment.objects.create(course_id=self.course,
                                                                     user_id=self.user)
        self.section_assignment = UserCourseAssignment.objects.create(course_id=self.course,
                                                                      user_id=self.user,
                                                                      section_id=self.section)

    def test_remove_no_user(self):
        self.assertEqual("user does not exist", remove_user_from(None, self.course),
                         "Failed to identify nonexistent user")

    def test_remove_no_course(self):
        self.assertEqual("invalid course input", remove_user_from(self.user, None),
                         "Failed to identify nonexistent course")