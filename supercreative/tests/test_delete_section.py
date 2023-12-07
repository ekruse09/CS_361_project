from django.test import TestCase
from supercreative.models import Section, User, UserCourseAssignment, Course
from supercreative.delete_section import delete_section


class MyTestCase(TestCase):
    def setUp(self):
        self.good_section = Section(section_id=1, course_id=1, section_type="LEC")
        self.good_user = User(user_id=1, email="test@uwm.edu", password="Testp@ass", role="Administrator",
                              first_name="testfirst", last_name="testlast", phone_number="5555555555",
                              address="testaddress")
        self.bad_user = User(user_id=1, email="test@uwm.edu", password="Testp@ass", role="TA",
                             first_name="testfirst", last_name="testlast", phone_number="5555555555",
                             address="testaddress")
        self.good_assign = UserCourseAssignment(user_id=1, section_id=1, course_id=1, section_type="LEC")

    def test_delete_section(self):
        self.assertTrue(delete_section(self.good_user, self.good_section),"Failed delete section")
        self.assertFalse(Section.objects.filter(section_id=1).exists(),"Failed section still exist")

    def test_role(self):
        self.assertTrue(delete_section(self.good_user, self.good_section),"Failed good user didn't delete")
        self.assertFalse(delete_section(self.bad_user, self.good_section), "Failed bad user did delete")

    def test_no_section(self):
        self.assertFalse(delete_section(self.good_user,""),"Failed no section pass")
        self.assertFalse(delete_section("",self.good_section),"Failed no user pass")

    def test_bad_parameter(self):
        self.assertFalse(delete_section(self.good_user,Section(section_id=-1, course_id=1, section_type="LEC")),
                         "Section_id is invalid")
        self.assertFalse(delete_section(self.good_user,Section(section_id=2, course_id=1, section_type="LEC")),
                         "Section does not exist")
    def test_UserCourseAssignement(self):
        self.assertTrue(delete_section(self.good_user,self.good_section),"Failed to delete section")
        self.assertFalse(UserCourseAssignment.section_id.objects.filter(self.good_section.section_id).exists(),
                         "Section exist on User_Course_Assignment")


