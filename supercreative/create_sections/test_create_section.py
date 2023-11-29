from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from supercreative.models import (Course, Section)
from supercreative.create_sections.section import create_section


class CreateSectionTest(TestCase):
    course = None

    def setUp(self):
        # variable values to use in the tests
        self.section_id = 801
        self.section_type = "lab"
        self.role = "administrator"

        # set up two mock courses
        self.course = Course.objects.create(course_name="Intro to Software Engineering", course_id=1,
                                            course_description="stuff", course_code="COMPSCI-361")

        self.course_two = Course.objects.create(course_name="System Programming", course_id=5,
                                                course_description="stuff", course_code="COMPSCI-337")

        # set up a mock section (to test for duplicates)
        self.section = Section.objects.create(section_id=803, course_id=self.course_two,
                                              section_type="discussion")

    def test_correct_section(self):
        # correctly create a section
        self.assertTrue(
            create_section(section_id=self.section_id, course=self.course, section_type=self.section_type,
                           role=self.role),
            "create_section did not return true when it should have.")

        # get created course and check its values
        created_section = Section.objects.get(section_id=self.section_id)

        self.assertEqual(created_section.section_id, self.section_id, "create_section did not correctly set the "
                                                                      "section_id")

        self.assertEqual(created_section.section_type, self.section_type, "create_course did not "
                                                                          "correctly set the "
                                                                          "section_type")

    # course must exist (course_id in database)
    def test_invalid_course_id(self):
        # attempt to create a section with various invalid course ids
        self.assertFalse(create_section(self.section_id, 3465423, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, None, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, "wrong", self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, -1, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(section_id=self.section_id)

    # section id must be a unique integer
    def test_invalid_section_id(self):
        # attempt to create a course with various invalid section ids
        self.assertFalse(create_section(-1, self.course.course_id, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(None, self.course.course_id, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section("wrong", self.course.course_id, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        # duplicate section_id
        self.assertFalse(create_section(self.section.section_id, self.course.course_id, self.section_type,
                                        self.role),
                         "create_section did not return false when it should have.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(course_id=self.course.course_id)

    # section type must be: lecture, lab, or discussion
    def test_invalid_section_type(self):
        # attempt to create a course with various invalid section types
        self.assertFalse(create_section(self.section_id, self.course.course_id, "wrong",
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, self.course.course_id, None,
                                        self.role),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, self.course.course_id, "",
                                        self.role),
                         "create_section did not return false when it should have.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(section_id=self.section_id)

    # must have admin privileges
    def test_invalid_role(self):
        # attempt to create a section with invalid user role
        self.assertFalse(create_section(self.section_id, self.course.course_id, self.section_type,
                                        "student"),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, self.course.course_id, self.section_type,
                                        None),
                         "create_section did not return false when it should have.")

        self.assertFalse(create_section(self.section_id, self.course.course_id, self.section_type,
                                        ""),
                         "create_section did not return false when it should have.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(section_id=self.section_id)
