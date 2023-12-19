from django.test import TestCase
from supercreative.models import Course, User, Section, UserCourseAssignment
from supercreative.course.assign_user import assign_user_to


class TestUserAssignment(TestCase):
    user = None
    course = None
    assignment = None
    section = None

    def setUp(self):
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.course = Course.objects.create(course_id=101, course_name="Introduction to Python",
                                            course_description="A basic course on Python programming",
                                            course_code="PY101")
        self.section = Section.objects.create(section_id=1, course_id=self.course, section_type="Lecture")
        pass

    def test_assignment(self):
        self.assertEqual(assign_user_to(self.user, self.course, self.section), "user successfully assigned to course "
                                                                               "and section", msg="Failed to create "
                                                                                                  "assignment")
        self.assertTrue(UserCourseAssignment.objects.filter(user_id=self.user, course_id=self.course,
                                                            section_id=self.section).exists(),
                        "Failed to assign course")

    def test_assignment_no_section(self):
        self.assertEqual(assign_user_to(self.user, self.course), "user successfully assigned to course and section",
                         msg="Failed to create assignment")
        self.assertTrue(UserCourseAssignment.objects.filter(user_id=self.user.user_id).exists())
        # print(UserCourseAssignment.objects.filter(user_id=self.user.user_id).exists())


class TestBadAssignment(TestCase):
    user = None
    course = None
    assignment = None
    section = None

    def setUp(self):
        self.user = User.objects.create(user_id=1, email="test@example.com",
                                        password="password123",
                                        role="student", first_name="John", last_name="Doe",
                                        phone_number="1234567890", address="123 Main St")
        self.course = Course.objects.create(course_id=101, course_name="Introduction to Python",
                                            course_description="A basic course on Python programming",
                                            course_code="PY101")
        self.section = Section.objects.create(section_id=1, course_id=self.course, section_type="Lecture")

    def test_no_course(self):
        self.assertEqual(assign_user_to(self.user, None, self.section), "user must have a course to be assigned to",
                         msg="Created null course assignment")

    def test_duplicate_assignment(self):
        UserCourseAssignment.objects.create(user_id=self.user, course_id=self.course,
                                            section_id=self.section,
                                            section_type=self.section.section_type)
        self.assertEqual(assign_user_to(self.user, self.course, self.section), "user already assigned to that course "
                                                                               "and section", msg="Created duplicate "
                                                                                                  "assignment")

    def test_duplicate_assignment_no_section(self):
        UserCourseAssignment.objects.create(user_id=self.user, course_id=self.course,
                                            section_id=None,
                                            section_type='')
        self.assertEqual(assign_user_to(self.user, self.course, None), "user already assigned to that course "
                                                                       "and section", msg="Created duplicate "
                                                                                          "assignment")
