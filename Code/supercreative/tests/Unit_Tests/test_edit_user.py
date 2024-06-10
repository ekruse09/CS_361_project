import os
from django.test import TestCase
from supercreative.user.user import create_user, edit_user, edit_user_with_skills
from supercreative.models import User, UserRole
from django.core.exceptions import ObjectDoesNotExist


class TestEditUser(TestCase):
    user = None
    new_user_info = None
    bad_user_id = None
    ta_user = None
    skills = "Mad skillz"

    def setUp(self):
        create_user("test@uwm.edu", "P@ssword123", UserRole.objects.create(role_name="Administrator").role_name, "John",
                    "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(email="test@uwm.edu")

        self.new_user_info = {"new_password": "p@SSWORD123",
                              "new_role": UserRole.objects.create(role_name="Instructor").role_name,
                              "new_first_name": "Jane",
                              "new_last_name": "Smith", "new_phone": "0987654321", "new_address": "456 Sesame St"}

        self.bad_user_id = 3

        create_user("ta@uwm.edu", 'P@ssword123', UserRole.objects.create(role_name="TA").role_name, "Jane", "Smith",
                    "0987654321", "456 Sesame St")

        self.ta_user = User.objects.get(email="ta@uwm.edu")

    def test_successful_edit_all(self):
        result = edit_user(self.user.user_id, self.new_user_info["new_password"], self.new_user_info["new_role"],
                           self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                           self.new_user_info["new_phone"], self.new_user_info["new_address"])
        self.assertEqual(result, "User edited successfully.")

        self.user = User.objects.get(user_id=self.user.user_id)

        self.assertEqual(self.user.password, self.new_user_info["new_password"], "Password failed to update")
        self.assertEqual(self.user.role_id.role_name, self.new_user_info["new_role"], "Role failed to update")
        self.assertEqual(self.user.first_name, self.new_user_info["new_first_name"], "First name failed to update")
        self.assertEqual(self.user.last_name, self.new_user_info["new_last_name"], "Last name failed to update")
        self.assertEqual(self.user.phone_number, self.new_user_info["new_phone"], "Phone number failed to update")
        self.assertEqual(self.user.address, self.new_user_info["new_address"], "Address failed to update")

    def test_bad_user_id(self):
        result = edit_user(self.bad_user_id, self.new_user_info["new_password"], self.new_user_info["new_role"],
                           self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                           self.new_user_info["new_phone"], self.new_user_info["new_address"])
        self.assertEqual(result, "User ID does not exist.")

    def test_bad_user_info(self):
        # bad password
        result = edit_user(self.user.user_id, "password", self.new_user_info["new_role"],
                           self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                           self.new_user_info["new_phone"], self.new_user_info["new_address"])
        self.assertEqual(result,
                         "Password must contain at least one uppercase letter, one lowercase letter, and one special "
                         "character.")

        # bad role
        result = edit_user(self.user.user_id, self.new_user_info["new_password"], "role",
                           self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                           self.new_user_info["new_phone"], self.new_user_info["new_address"])
        self.assertEqual(result, "Invalid role selected.")

        # bad number
        result = edit_user(self.user.user_id, self.new_user_info["new_password"], self.new_user_info["new_role"],
                           self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                           "123-456-789", self.new_user_info["new_address"])
        self.assertEqual(result, "Phone number must be 10 digits.")

    def test_edit_skills(self):
        result = edit_user_with_skills(self.user.user_id,
                                       self.user.password,
                                       self.user.role_id.role_name,
                                       self.user.first_name,
                                       self.user.last_name,
                                       self.user.phone_number,
                                       self.user.address,
                                       self.skills)

        self.assertEqual(result, "User edited successfully.", "Failed to edit user skills")
        self.assertEqual(User.objects.get(user_id=self.user.user_id).skills, self.skills,
                         "Failed to update skills")
