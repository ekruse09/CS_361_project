from django.test import TestCase
from supercreative.models import Course, Section
from supercreative.course.course import delete_course
from django.core.exceptions import ObjectDoesNotExist


class TestCourseDelete(TestCase):
    bad_course = None
    good_course = None
    section1 = None
    section2 = None

    def setUp(self):
        self.bad_course = Course.objects.create(course_id=101, course_name="Introduction to Python",
                                                course_description="A basic course on Python programming",
                                                course_code="PY101")

        self.good_course = Course.objects.create(course_id=201, course_name="Intermediate Python Programming",
                                                 course_description="An intermediate course on Python programming",
                                                 course_code="PY101")
        self.section1 = Section.objects.create(section_id=1, course_id=self.bad_course, section_type="Lecture")
        self.section2 = Section.objects.create(section_id=2, course_id=self.bad_course, section_type="Lab")

    def test_successful_delete(self):
        self.assertTrue(delete_course(self.good_course), "Failed to delete course")
        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(course_id=self.good_course.course_id)

    def test_failed_delete(self):
        self.assertFalse(delete_course(self.bad_course), "Deleted course with sections")
