from django.test import TestCase
from supercreative.models import Section, UserCourseAssignment
from supercreative.delete_section.delete_section import delete_section


class MyTestCase(TestCase):
    def setUp(self):
        self.good_section = Section(section_id=1, course_id=1, section_type="LEC")
        self.good_assign = UserCourseAssignment(user_id=1, section_id=1, course_id=1, section_type="LEC")

    def test_delete_section(self):
        self.assertEqual(delete_section(self.good_section), "Section deletion was successful",
                         "Failed delete section")
        self.assertFalse(Section.objects.filter(section_id=1).exists(), "Failed section still exist")
        self.assertFalse(UserCourseAssignment.section_id.objects.filter(self.good_section.section_id).exists(),
                         "Section exist on User_Course_Assignment")

    def test_no_parameter(self):
        self.assertEqual(delete_section(""), "No Section detected", "Failed no section pass")

    def test_non_existing_section(self):
        self.assertEqual(delete_section(Section(section_id=-1, course_id=1, section_type="LEC")),
                         "Section deletion was successful", "Section_id is invalid")
        self.assertEqual(delete_section(Section(section_id=2, course_id=1, section_type="LEC")),
                         "Section does not exist", "Section does not exist")
