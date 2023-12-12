from django.test import TestCase
from supercreative.models import (Course)
from supercreative.course.course import edit_course, create_course


class TestCourseEdit(TestCase):
    base_course = None
    new_course_values = None
    existing_course = None

    def setUp(self):
        create_course("Introduction to Python",
                      "A basic course on Python programming",
                      "PY101")
        self.base_course = Course.objects.get(course_name="Introduction to Python")
        self.new_course_values = {"course_name": "New Intro to Python",
                                  "course_description": "An up to date introductory course on Python",
                                  "good_course_code": "PY102", "bad_course_code": "PY151"}
        create_course("Intermediate Python Programming",
                      "A basic course on Python programming",
                      "PY151")
        self.existing_course = Course.objects.get(course_name="Intermediate Python Programming")

    def test_successful_edit_all(self):
        # Edit all
        self.assertTrue(edit_course(self.base_course.course_id, self.new_course_values["course_name"],
                                    self.new_course_values["course_description"],
                                    self.new_course_values["good_course_code"]))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.new_course_values["course_name"], "Course name change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.new_course_values["course_description"], "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.new_course_values["good_course_code"], "Course code change failed")

    def test_successful_edit_name(self):
        # Edit name only
        self.assertTrue(edit_course(self.base_course.course_id, self.new_course_values["course_name"], '', ''))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.new_course_values["course_name"], "Course name change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")

    def test_successful_edit_description(self):
        # Edit description only
        self.assertTrue(edit_course(self.base_course.course_id, '', self.new_course_values["course_description"], ''))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.new_course_values["course_description"], "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code changed")

    def test_successful_edit_code(self):
        # Edit code only
        self.assertTrue(edit_course(self.base_course.course_id, '', '', self.new_course_values["good_course_code"]))
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.new_course_values["good_course_code"], "Course code change failed")

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
