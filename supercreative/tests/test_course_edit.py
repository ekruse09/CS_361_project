from django.test import TestCase
from supercreative.models import (Course)
from supercreative.create_course.course import edit_course

class TestCourseEdit(TestCase):
    base_course = None
    updated_course = None
    existing_course = None
    def setUp(self):
        self.base_course = Course.objects.create(course_id=101, course_name="Introduction to Python",
                              course_description="A basic course on Python programming",
                              course_code="PY101")
        self.updated_course = {"course_name":"New Intro to Python",
                               "course_description":"An up to date introductory course on Python",
                               "good_course_code":"PY102", "bad_course_code":"PY151"}
        self.existing_course = Course.objects.create(course_id=102, course_name="Intermediate Python Programming",
                              course_description="A basic course on Python programming",
                              course_code="PY151")

    def test_successful_edit_all(self):
        # Edit all
        self.assertTrue(edit_course(self.base_course.course_id, self.updated_course["course_name"],
                    self.updated_course["course_description"], self.updated_course["good_course_code"]))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.updated_course["course_name"], "Course name change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.updated_course["course_description"], "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.updated_course["good_course_code"], "Course code change failed")

    def test_successful_edit_name(self):
        # Edit name only
        self.assertTrue(edit_course(self.base_course.course_id, self.updated_course["course_name"], '', ''))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.updated_course["course_name"], "Course name change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")

    def test_successful_edit_description(self):
        # Edit description only
        self.assertTrue(edit_course(self.base_course.course_id, '', self.updated_course["course_description"], ''))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.updated_course["course_description"], "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")

    def test_successful_edit_code(self):
        # Edit code only
        self.assertTrue(edit_course(self.base_course.course_id, '', '', self.updated_course["good_course_code"]))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.updated_course["good_course_code"], "Course code change failed")

    def test_duplicates(self):
        # Duplicate name
        self.assertFalse(edit_course(self.base_course.course_id, self.existing_course.course_name, '', ''))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")

        # Duplicate description allowed
        self.assertTrue(edit_course(self.base_course.course_id, '', self.existing_course.course_description, ''))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.existing_course.course_description, "Course description not changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")

        self.assertFalse(edit_course(self.base_course.course_id, '', '', self.existing_course.course_code))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")