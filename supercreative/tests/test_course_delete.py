from django.test import TestCase
from supercreative.models import Course, Section
from supercreative.course.course import delete_course, create_course
from django.core.exceptions import ObjectDoesNotExist


class TestCourseDelete(TestCase):
    bad_course = None
    good_course = None
    section1 = None
    section2 = None

    def setUp(self):
        create_course(101, "Introduction to Python",
                      "A basic course on Python programming",
                      "PY101")
        self.bad_course = Course.objects.get(course_id=101)

        create_course(201, "Intermediate Python Programming",
                      "An intermediate course on Python programming",
                      "PY201")
        self.good_course = Course.objects.get(course_id=201)

        # Missing integration tests
        self.section1 = Section.objects.create(section_id=1, course_id=self.bad_course, section_type="Lecture")
        self.section2 = Section.objects.create(section_id=2, course_id=self.bad_course, section_type="Lab")

    def test_successful_delete(self):
        self.assertTrue(delete_course(self.good_course), "Failed to delete course")
        with self.assertRaises(ObjectDoesNotExist):
            Course.objects.get(course_id=self.good_course.course_id)

    def test_failed_delete(self):
        self.assertFalse(delete_course(self.bad_course), "Deleted course with sections")
