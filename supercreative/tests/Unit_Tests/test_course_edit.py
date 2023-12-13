from django.test import TestCase
from supercreative.models import (Course)
from supercreative.Course.course import edit_course, create_course


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
        result = edit_course(self.base_course.course_id, self.new_course_values["course_name"],
                             self.new_course_values["course_description"],
                             self.new_course_values["good_course_code"])
        self.assertEqual(result, "Course edited successfully.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.new_course_values["course_name"], "Course name change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.new_course_values["course_description"], "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.new_course_values["good_course_code"], "Course code change failed")

    def test_successful_edit_name(self):
        # Edit name only
        result = edit_course(self.base_course.course_id, self.new_course_values["course_name"], '', '')
        self.assertEqual(result, "Course edited successfully.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.new_course_values["course_name"], "Course name change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code should not have changed")

    def test_successful_edit_description(self):
        # Edit description only
        result = edit_course(self.base_course.course_id, '', self.new_course_values["course_description"], '')
        self.assertEqual(result, "Course edited successfully.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.new_course_values["course_description"], "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code should not have changed")

    def test_successful_edit_code(self):
        # Edit code only
        result = edit_course(self.base_course.course_id, '', '', self.new_course_values["good_course_code"])
        self.assertEqual(result, "Course edited successfully.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.new_course_values["good_course_code"], "Course code change failed")

    def test_duplicate_name(self):
        # Duplicate name
        result = edit_course(self.base_course.course_id, self.existing_course.course_name, '', '')
        self.assertEqual(result, "Course code, or name already exists.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code should not have changed")

    # Duplicate description allowed
    def test_duplicate_description(self):
        result = edit_course(self.base_course.course_id, '', self.existing_course.course_description, '')
        self.assertEqual(result, "Course edited successfully.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.existing_course.course_description, "Course description change failed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code should not have changed")

    def test_duplicate_code(self):
        result = edit_course(self.base_course.course_id, '', '', self.existing_course.course_code)
        self.assertEqual(result, "Course code, or name already exists.")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_name,
                         self.base_course.course_name, "Course name should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_description,
                         self.base_course.course_description, "Course description should not have changed")
        self.assertEqual(Course.objects.get(course_id=self.base_course.course_id).course_code,
                         self.base_course.course_code, "Course code should not have changed")

