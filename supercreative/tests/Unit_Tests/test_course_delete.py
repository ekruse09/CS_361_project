from django.test import TestCase
from supercreative.models import Course, Section, SectionType
from supercreative.course.course import delete_course, create_course
from django.core.exceptions import ObjectDoesNotExist


class TestCourseDelete(TestCase):
    bad_course = None
    good_course = None
    section1 = None
    section2 = None
    section_type1 = None
    section_type2 = None

    def setUp(self):
        create_course("Introduction to Python",
                      "A basic course on Python programming",
                      "PY101")
        self.bad_course = Course.objects.get(course_name="Introduction to Python")

        create_course("Intermediate Python Programming",
                      "An intermediate course on Python programming",
                      "PY201")
        self.good_course = Course.objects.get(course_name="Intermediate Python Programming")

        self.section_type1 = SectionType.objects.create(section_type_name="Lecture")
        self.section_type2 = SectionType.objects.create(section_type_name="Lab")

        self.section1 = Section.objects.create(course_id=self.bad_course, section_type=self.section_type1)
        self.section2 = Section.objects.create(course_id=self.bad_course, section_type=self.section_type2)

    def test_successful_delete(self):
        self.assertTrue(delete_course(self.good_course), "Failed to delete course")
        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(course_id=self.good_course.course_id)

    def test_delete_course_with_sections(self):
        delete_course(self.bad_course)
        self.assertFalse(Section.objects.filter(section_id=self.section1.section_id).exists(), "failed to delete sections")
