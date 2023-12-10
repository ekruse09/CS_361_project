from django.test import TestCase
from supercreative.models import Section, Course, UserCourseAssignment
from supercreative.delete_section.Edit_section import edit_section

class TestEditSection(TestCase):
    def setUp(self):
        self.exist_section = Section(section_id=1, course_id=1, section_type="LEC")
        self.double_section = Section(section_id=3, course_id=1, section_type="LEC")
        self.exist_course = Course(course_id=1,course_name="test",course_description="test",course_code="test")
        self.exist_course2 = Course(course_id=2, course_name="test2", course_description="test2", course_code="test2")
        self.exist_Userassignment = UserCourseAssignment(user_id=1, section_id=1, course_id=1, section_type="LEC")

    def test_edit_section(self):
        self.assertTrue(edit_section(1,2,1,2, "LAB"))
        self.assertEqual(self.exist_section.section_id,2)
        self.assertEqual(self.exist_section.course_id,2)
        self.assertEqual(self.exist_section.section_type,"LAB")
        self.assertEqual(self.exist_Userassignment.section_id,2)
        self.assertEqual(self.exist_Userassignment.course_id, 2)
        self.assertEqual(self.exist_Userassignment.section_type, "LAB")

    def test_nonexist(self):
        self.assertFalse(edit_section(2,1,1,2,"LAB"))
        self.assertFalse(edit_section(1,1,3,2,"LAB"))

    def test_bad_parameter(self):
        self.assertFalse(edit_section(-1,1,1,2,"LAB"))
        self.assertFalse(edit_section(1, 1, -1, 2, "LAB"))
        self.assertFalse(edit_section(1, 1, 1, 2, "BAD"))
        self.assertFalse(edit_section("Bad", 1, 1, 2, "LAB"))
        self.assertFalse(edit_section(1, 3, 1, 2, "LAB"))
