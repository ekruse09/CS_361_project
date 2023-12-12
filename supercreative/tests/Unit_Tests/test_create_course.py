from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from supercreative.models import (User, Course)
from supercreative.course.course import create_course


class CreateCourseTest(TestCase):
    course = None
    role = None

    def setUp(self):
        # variable values to use in the tests
        self.course_name = "Intro to Software Engineering"
        self.course_description = "stuff"
        self.course_code = "COMPSCI-361"
        self.role = "administrator"
        self.created_course = None

    def test_correct_course(self):
        # correctly create a course
        self.assertEqual(create_course(self.course_name, self.course_description, self.course_code),
                         "Course created successfully.",
                         "create_course did not return true when it should have.")
        # self.assertTrue(create_course(self.course_id, self.course_name, self.course_description,
        #                               self.course_code),
        #                 "create_course did not return true when it should have.")

        self.assertTrue(Course.objects.filter(course_name=self.course_name).exists(), "Didn't create course")

        self.created_course = Course.objects.get(course_name=self.course_name)

        self.assertEqual(self.created_course.course_name, self.course_name,
                         "create_course did not correctly set the course_name")

        self.assertEqual(self.created_course.course_description, self.course_description,
                         "create_course did not correctly set the course_description")

        self.assertEqual(self.created_course.course_code, self.course_code,
                         "create_course did not correctly set the course_code")

    def test_invalid_course_name(self):
        # attempt to create a course with various invalid course names
        self.assertEqual(create_course(1, self.course_description, self.course_code),
                         "Course name must be a string.",
                         "create_course didn't return the correct error message for an invalid name.")

        response = create_course(True, self.course_description, self.course_code)
        self.assertEqual(response,
                         "Course name must be a string.",
                         "create_course did not return the correct message")

        self.assertEqual(create_course(None, self.course_description,
                                       self.course_code),
                         "Course name must be a string.",
                         "create_course did not return the correct message")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Course.objects.get(course_name=self.course_name)

    def test_invalid_course_description(self):
        # Attempt to create a course with a non-string course description
        self.assertEqual(create_course(self.course_name, 1, self.course_code),
                         "Course description must be a string.",
                         "create_course didn't return the correct error message for a numeric description.")

        # Attempt to create a course with a boolean as course description
        self.assertEqual(create_course(self.course_name, False, self.course_code),
                         "Course description must be a string.",
                         "create_course didn't return the correct error message for a boolean description.")

        # Attempt to create a course with None as course description
        self.assertEqual(create_course(self.course_name, None, self.course_code),
                         "Course description must be a string.",
                         "create_course didn't return the correct error message for a None description.")

        # Make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="Course with invalid description should not exist"):
            Course.objects.get(course_name=self.course_name)

    def test_invalid_course_code(self):
        # Attempt to create a course with a non-string course code
        self.assertEqual(create_course(self.course_name, self.course_description, 1),
                         "Course code must be a string.",
                         "create_course didn't return the correct error message for a numeric course code.")

        # Attempt to create a course with a boolean as course code
        self.assertEqual(create_course(self.course_name, self.course_description, False),
                         "Course code must be a string.",
                         "create_course didn't return the correct error message for a boolean course code.")

        # Attempt to create a course with None as course code
        self.assertEqual(create_course(self.course_name, self.course_description, None),
                         "Course code must be a string.",
                         "create_course didn't return the correct error message for a None course code.")

        # Make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="Course with invalid code should not exist"):
            Course.objects.get(course_name=self.course_name)

    def test_duplicates(self):
        # Create a course
        self.assertEqual(create_course(self.course_name, self.course_description, self.course_code),
                         "Course created successfully.",
                         "create_course did not return the expected success message on initial course creation.")

        # Try to create additional courses with duplicate course name
        self.assertEqual(create_course(self.course_name, self.course_description, "different course code"),
                         "Course name, or code already exists.",
                         "create_course didn't return the correct error message for duplicate course name.")

        # Try to create additional courses with duplicate course code
        self.assertEqual(create_course("different course name", self.course_description, self.course_code),
                         "Course name, or code already exists.",
                         "create_course didn't return the correct error message for duplicate course code.")

        # Make sure none of the courses with duplicate values were created
        with self.assertRaises(ObjectDoesNotExist, msg="Course with different course name should not exist"):
            Course.objects.get(course_name="different course name")

        with self.assertRaises(ObjectDoesNotExist, msg="Course with ID 3 should not exist"):
            Course.objects.get(course_id=3)

        with self.assertRaises(ObjectDoesNotExist, msg="Course with different course code should not exist"):
            Course.objects.get(course_code="different course code")
