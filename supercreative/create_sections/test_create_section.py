from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from supercreative.models import (User, Course, Section)
from supercreative.create_sections.section import create_section


class CreateSectionTest(TestCase):
    course = None

    # done
    def setUp(self):
        # variable values to use in the tests
        self.section_id = 801
        self.section_type = "lab"
        self.role = "administrator"

        # set up a mock course
        self.course = Course.objects.create(course_name="Intro to Software Engineering", course_id=1,
                                            course_description="stuff", course_code="COMPSCI-361")

    # done
    def test_correct_course(self):
        # correctly create a section
        self.assertTrue(
            create_section(section_id=self.section_id, course_id=self.course.course_id, section_type=self.section_type,
                           role=self.role),
            "create_section did not return true when it should have.")

        # get created course and check its values
        created_section = Section.objects.get(section_id=self.section_id)

        self.assertEqual(created_section.course_id, self.course.course_id, "create_section did not correctly set the "
                                                                           "course_id")

        self.assertEqual(created_section.section_id, self.section_id, "create_section did not correctly set the "
                                                                      "section_id")

        self.assertEqual(created_section.section_type, self.section_type, "create_course did not "
                                                                          "correctly set the "
                                                                          "section_type")
    '''
    # TODO
    # course must exist
    def test_invalid_course_id(self):
        # attempt to create a course with various invalid course ids
        self.assertFalse(create_course("wrong", self.course_name, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course("1", self.course_name, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(None, self.course_name, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(-1, self.course_name, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Course.objects.get(course_name=self.course_name)

    # TODO
    # make sure to test for duplicate section_ids
    def test_invalid_section_id(self):
        # attempt to create a course with various invalid course names
        self.assertFalse(create_course(self.course_id, 1, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course_id, True, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course_id, None, self.course_description,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Course.objects.get(course_id=self.course_id)

    # TODO
    # section type must be lecture, lab, or discussion
    def test_invalid_section_type(self):
        # attempt to create a course with various invalid course descriptions
        self.assertFalse(create_course(self.course_id, self.course_name, 1,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course_id, self.course_name, False,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course_id, self.course_name, None,
                                       self.course_code, self.role),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Course.objects.get(course_id=self.course_id)


    # TODO
    # must have admin privileges
    def test_invalid_role(self):
        # attempt to create a course with invalid user role
        self.assertFalse(create_course(self.course_id, self.course_name, self.course_description,
                                       self.course_code, ""),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course_id, self.course_name, self.course_description,
                                       self.course_code, "student"),
                         "create_course did not return false when it should have.")

        self.assertFalse(create_course(self.course_id, self.course_name, self.course_description,
                                       self.course_code, None),
                         "create_course did not return false when it should have.")

        # make sure the invalid courses weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Course.objects.get(course_id=self.course_id)
    '''
