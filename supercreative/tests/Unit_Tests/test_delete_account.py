from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from supercreative.models import User, Course, Section, UserCourseAssignment, UserRole, SectionType
from supercreative.user import user


class TestAccountDelete(TestCase):
    admin_user = None
    student_user = None
    course1 = None
    course2 = None
    section1 = None
    section2 = None
    role = None

    def setUp(self):
        # create an admin user
        self.role = UserRole.objects.create(role_name="Administrator")
        self.admin_user = User.objects.create(email="test@example.com",
                                              password="password123",
                                              role_id=self.role,
                                              first_name="John",
                                              last_name="Doe",
                                              phone_number="1234567890",
                                              address="123 Main St")

        # create a couple of courses
        self.course1 = Course.objects.create(course_name="Course 1", course_description="stuff",
                                             course_code="COURSE-1")
        self.course2 = Course.objects.create(course_name="Course 2", course_description="stuff",
                                             course_code="COURSE-2")

        # create a couple of sections
        self.section1 = Section.objects.create(course_id=self.course1, section_type=SectionType.objects.create(section_type_name="Lecture"))
        self.section2 = Section.objects.create(course_id=self.course2, section_type=SectionType.objects.create(section_type_name="Lab"))

        # assign the admin user to the sections
        UserCourseAssignment.objects.create(user_id=self.admin_user, section_id=self.section1, course_id=self.course1,
                                            section_type=self.section1.section_type)
        UserCourseAssignment.objects.create(user_id=self.admin_user, section_id=self.section2, course_id=self.course2,
                                            section_type=self.section2.section_type)

    def test_successful_delete(self):
        self.assertEqual(user.delete_user(self.admin_user.user_id), "Successfully deleted user.", "delete user should've returned "
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
        self.assertEqual(user.delete_user(24),"User not found.", "Deleted a non-existent user")
