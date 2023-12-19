from django.test import TestCase
from supercreative.models import Course, User, Section, UserCourseAssignment, UserRole, SectionType
from supercreative.course.user_assignments import assign_user_to


class TestAssignUserTo(TestCase):
    user = None
    other_user = None
    course = None
    assignment = None
    section = None

    def setUp(self):
        self.user = User.objects.create(email="test@example.com",
                                        password="password123",
                                        role_id=UserRole.objects.create(role_name="Instructor"),
                                        first_name="John",
                                        last_name="Doe",
                                        phone_number="1234567890",
                                        address="123 Main St")
        self.other_user = User.objects.create(email="test2@example.com",
                                        password="password123",
                                        role_id=UserRole.objects.create(role_name="Instructor"),
                                        first_name="Jane",
                                        last_name="Doe",
                                        phone_number="1234567890",
                                        address="123 Main St")
        self.course = Course.objects.create(course_name="Introduction to Python",
                                            course_description="A basic course on Python programming",
                                            course_code="PY101")
        self.section = Section.objects.create(course_id=self.course,
                                              section_type=SectionType.objects.create(section_type_name="Lecture"))

    def test_assignment(self):
        self.assertEqual(assign_user_to(self.user, self.course, self.section),
                         "successfully created the user assignment",
                         msg="Failed to create assignment")
        self.assertTrue(UserCourseAssignment.objects.filter(user_id=self.user,
                                                            course_id=self.course,
                                                            section_id=self.section).exists(),
                        "Failed to assign course")

    def test_assignment_no_section(self):
        self.assertEqual(assign_user_to(self.user, self.course), "successfully created the user assignment",
                         msg="Failed to create assignment")
        self.assertTrue(UserCourseAssignment.objects.filter(user_id=self.user.user_id).exists())

    def test_existing_assignment(self):
        self.assertEqual(assign_user_to(self.other_user, self.course, self.section),
                         "successfully created the user assignment",
                         msg="Failed to create assignment")
        self.assertTrue(UserCourseAssignment.objects.filter(user_id=self.other_user,
                                                            course_id=self.course,
                                                            section_id=self.section).exists(),
                        "Failed to create assignment")

        self.assertEqual(assign_user_to(self.user, self.course, self.section),
                         "successfully created the user assignment",
                         msg="Failed to create assignment")
        self.assertTrue(UserCourseAssignment.objects.filter(user_id=self.user,
                                                            course_id=self.course,
                                                            section_id=self.section).exists(),
                        "Failed to assign course")


class TestBadAssignment(TestCase):
    user = None
    course = None
    assignment = None
    section = None

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

    def test_no_course(self):
        self.assertEqual(assign_user_to(self.user, None, self.section),
                         "invalid course input", msg="Created null course assignment")

    def test_duplicate_assignment(self):
        UserCourseAssignment.objects.create(user_id=self.user, course_id=self.course,
                                            section_id=self.section,
                                            section_type=self.section.section_type)
        self.assertEqual(assign_user_to(self.user, self.course, self.section),
                         "assignment already exists", msg="Created duplicate assignment")

    def test_duplicate_assignment_no_section(self):
        UserCourseAssignment.objects.create(user_id=self.user, course_id=self.course,
                                            section_id=None,
                                            section_type=None)
        self.assertEqual(assign_user_to(self.user, self.course, None),
                         "assignment already exists", msg="Created null course assignment")
