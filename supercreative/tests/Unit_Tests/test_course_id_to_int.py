from django.test import TestCase

# Adjust the import path according to where course_id_to_int function is located in your project
from supercreative.Course.course import course_id_to_int

class CourseIdToIntTest(TestCase):

    def test_valid_integer_input(self):
        # Test with a valid integer input as a string
        self.assertEqual(course_id_to_int("123"), 123, "Failed to convert valid integer string to int")

    def test_valid_integer(self):
        # Test with a valid integer
        self.assertEqual(course_id_to_int(456), 456, "Failed to process valid integer")

    def test_invalid_input(self):
        # Test with a string that cannot be converted to an integer
        self.assertIsNone(course_id_to_int("invalid"), "Failed to return None for a non-integer string")

    def test_none_input(self):
        # Test with None as input
        self.assertIsNone(course_id_to_int(None), "Failed to return None for None input")

    def test_float_input(self):
        # Test with a float as input
        self.assertEqual(course_id_to_int(123.45), 123, "Failed to return None for float input")

    # Additional test cases can be added as needed
