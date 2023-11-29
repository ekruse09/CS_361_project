from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from supercreative.models import User, Course, Section, UserCourseAssignment
from supercreative.CreateAccount.delete_account import delete_user


class TestAccountDelete(TestCase):
    admin_user = None
    student_user = None
    course1 = None
    course2 = None
    section1 = None
    section2 = None

    def setUp(self):
        # create an admin user
        self.admin_user = User.objects.create(user_id=1, email="test@example.com",
                                              password="password123",
                                              role="administrator", first_name="John", last_name="Doe",
                                              phone_number="1234567890", address="123 Main St")

        # create a couple of courses
        self.course1 = Course.objects.create(course_id=1, course_name="Course 1", course_description="stuff",
                                             course_code="COURSE-1")
        self.course2 = Course.objects.create(course_id=2, course_name="Course 2", course_description="stuff",
                                             course_code="COURSE-2")

        # create a couple of sections
        self.section1 = Section.objects.create(section_id=1, course_id=self.course1, section_type="Lecture")
        self.section2 = Section.objects.create(section_id=2, course_id=self.course2, section_type="Lab")

        # assign the admin user to the sections
        UserCourseAssignment.objects.create(user_id=self.admin_user, section_id=self.section1, course_id=self.course1,
                                            section_type="Lecture")
        UserCourseAssignment.objects.create(user_id=self.admin_user, section_id=self.section2, course_id=self.course2,
                                            section_type="Lab")

        # create a student user
        self.student_user = User.objects.create(user_id=2, email="student@example.com",
                                                password="password123",
                                                role="student", first_name="Jane", last_name="Doe",
                                                phone_number="0987654321", address="321 Main St")

    def test_successful_delete(self):
        self.assertTrue(delete_user(self.admin_user.user_id), "delete user should've returned "
                                                              "true here!")

        # check to see if the user was actually deleted from the Users table
        with self.assertRaises(ObjectDoesNotExist, msg="failed to delete user."):
            User.objects.get(user_id=self.admin_user.user_id)

        self.assertEqual(UserCourseAssignment.objects.count(), 0, "UserCourseAssignment entries were not "
                                                                  "deleted.")
        # Assuming each course assignment was counted as a single entry, subtracting 2 represents the removal of both
        # assignments.

    def test_no_user(self):
        # trying to delete a user that doesn't exist
        self.assertFalse(delete_user(24), "delete user should've "
                                          "returned false here!")
