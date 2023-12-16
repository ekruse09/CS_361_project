from django.test import TestCase
from supercreative.models import Course, Section, SectionType
from supercreative.create_sections.section import create_section


class CreateSectionTest(TestCase):
    course = None
    course_two = None
    section = None

    def setUp(self):
        # variable values to use in the tests
        self.section_id = 801
        self.section_type = SectionType.objects.create(section_type_name="lab")

        # set up a mock user
        # set up two mock courses
        self.course = Course.objects.create(course_name="Intro to Software Engineering",
                                            course_description="stuff", course_code="COMPSCI-361")

        self.course_two = Course.objects.create(course_name="System Programming",
                                                course_description="stuff", course_code="COMPSCI-337")

        # set up a mock section (to test for duplicates)
        self.section = Section.objects.create(course_id=self.course_two,
                                              section_type=SectionType.objects.create(
                                                  section_type_name="discussion").section_type_name)

    def test_correct_section(self):
        self.assertEqual(create_section(self.course, self.section_type.section_type_name),
                         "section was successfully created")
        self.assertEqual(Section.objects.all().count(), 2, "create_course did not correctly create the section")

    # course must exist
    def test_invalid_course(self):
        # attempt to create a section with various invalid courses
        self.assertEqual(create_section(3465423, self.section_type.section_type_name),
                         "invalid input for course",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(None, self.section_type.section_type_name),
                         "invalid input for course",
                         "create_section did return the correct message.")

        self.assertEqual(create_section("wrong", self.section_type.section_type_name),
                         "invalid input for course",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(-1, self.section_type.section_type_name),
                         "invalid input for course",
                         "create_section did return the correct message.")

        # make sure the invalid sections weren't created
        self.assertEqual(Section.objects.all().count(), 1, "create_course created a section when it shouldn't have")

    def test_invalid_section_type(self):
        # attempt to create a course with various invalid section types
        self.assertEqual(create_section(self.course, "DISCUSSION", ),
                         "section type is not valid",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.course, None, ),
                         "section type is not valid",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.course, "Lab", ),
                         "section type is not valid",
                         "create_section did return the correct message.")

        # make sure the invalid sections weren't created
        self.assertEqual(Section.objects.all().count(), 1, "create_course created a section when it shouldn't have")
