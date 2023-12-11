from django.test import TestCase
from supercreative.models import Section, UserCourseAssignment, Course, User
from supercreative.delete_section.delete_section import delete_section


class MyTestCase(TestCase):
    def setUp(self):
        self.good_user = User(user_id=1, email="test@uwm.edu", password="test", role="Administrator", first_name="testfirst",
                              last_name="testlast", phone_number="5555555555", address="123")
        self.good_course = Course(course_id=1, course_name="test", course_description="test", course_code="test")
        self.good_course.save()
        self.good_section = Section(section_id=1, course_id=self.good_course, section_type="LEC")
        self.good_section.save()
        self.good_assign = UserCourseAssignment(user_id=self.good_user, section_id=self.good_section, course_id=self.good_course, section_type="LEC")

    def test_delete_section(self):

        self.assertEqual(delete_section(self.good_section.section_id), "Section deletion was successful",
                         "Failed delete section")
        self.assertFalse(Section.objects.filter(section_id=1).exists(), "Failed section still exist")
        self.assertFalse(UserCourseAssignment.objects.filter(section_id=self.good_section).exists(),
                         "Section exist on User_Course_Assignment")

    def test_no_parameter(self):
        self.assertEqual(delete_section(""), "No Section detected", "Failed no section pass")

    def test_non_existing_section(self):
        self.assertEqual(delete_section(-1),
                         "Section does not exist", "Section_id is invalid")
        self.assertEqual(delete_section(2),
                         "Section does not exist", "Section does not exist")
