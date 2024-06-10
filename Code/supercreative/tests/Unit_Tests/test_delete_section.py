from django.test import TestCase
from supercreative.models import Section, UserCourseAssignment, Course, User, UserRole, SectionType
from supercreative.section.section import delete_section


class TestDeleteSection(TestCase):
    def setUp(self):
        self.good_user = User.objects.create(email="test@uwm.edu",
                              password="test",
                              role_id=UserRole.objects.create(role_name="Administrator"),
                              first_name="testfirst",
                              last_name="testlast",
                              phone_number="5555555555",
                              address="123")
        self.good_course = Course.objects.create(course_name="test",
                              course_description="test",
                              course_code="test")
        self.good_section = Section.objects.create(course_id=self.good_course, section_type=SectionType.objects.create(section_type_name="Lecture"))
        self.good_assign = UserCourseAssignment.objects.create(user_id=self.good_user,
                                                               section_id=self.good_section,
                                                               course_id=self.good_course,
                                                               section_type=SectionType.objects.create(section_type_name="Lecture"))

    def test_delete_section(self):

        self.assertEqual(delete_section(self.good_course.course_id,self.good_section.section_id), "Section deletion was successful",
                         "Failed delete section")
        self.assertFalse(Section.objects.filter(course_id=self.good_section.course_id,section_id=self.good_section.section_id).exists(), "Failed section still exist")
        self.assertFalse(UserCourseAssignment.objects.filter(section_id=self.good_section).exists(),
                         "Section exist on User_Course_Assignment")

    def test_no_parameter(self):
        self.assertEqual(delete_section(self.good_section.course_id,None), "Section does not exist", "Failed no section pass")

    def test_non_existing_section(self):
        self.assertEqual(delete_section(self.good_section.course_id,-1),
                         "Section does not exist", "Section_id is invalid")
        self.assertEqual(delete_section(self.good_section.course_id,2),
                         "Section does not exist", "Section does not exist")
