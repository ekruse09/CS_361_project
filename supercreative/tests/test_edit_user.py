import os
from django.test import TestCase
from supercreative.user.user import create_user, edit_user
from supercreative.models import User
from django.core.exceptions import ObjectDoesNotExist


class TestEditUser(TestCase):
    user = None
    new_user_info = None
    bad_user_id = None

    def setUp(self):
        create_user(1, "test@uwm.edu", "P@ssword123", "ADMINISTRATOR", "John", "Doe",
                    "1234567890", "123 Main St")
        self.user = User.objects.get(user_id=1)

        self.new_user_info = {"new_password": "p@SSWORD123", "new_role": "TA", "new_first_name": "Jane",
                              "new_last_name": "Smith", "new_phone": "0987654321", "new_address": "456 Sesame St"}
        self.bad_user_id = 3

    def test_successful_edit_all(self):
        edit_user(self.user.user_id, self.new_user_info["new_password"], self.new_user_info["new_role"],
                  self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                  self.new_user_info["new_phone"], self.new_user_info["new_address"])

        self.user = User.objects.get(user_id=self.user.user_id)

        self.assertEqual(self.user.password, self.new_user_info["new_password"], "Password failed to update")
        self.assertEqual(self.user.role, self.new_user_info["new_role"], "Role failed to update")
        self.assertEqual(self.user.first_name, self.new_user_info["new_first_name"], "First name failed to update")
        self.assertEqual(self.user.last_name, self.new_user_info["new_last_name"], "Last name failed to update")
        self.assertEqual(self.user.phone_number, self.new_user_info["new_phone"], "Phone number failed to update")
        self.assertEqual(self.user.address, self.new_user_info["new_address"], "Address failed to update")

    def test_bad_user_id(self):
        self.assertFalse(edit_user(self.bad_user_id, self.new_user_info["new_password"], self.new_user_info["new_role"],
                                   self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                                   self.new_user_info["new_phone"], self.new_user_info["new_address"]))

    def test_bad_user_info(self):
        # bad password
        self.assertFalse(edit_user(self.user.user_id, "password", self.new_user_info["new_role"],
                      self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                      self.new_user_info["new_phone"], self.new_user_info["new_address"]), "Allowed bad password")

        # bad role
        self.assertFalse(edit_user(self.user.user_id, self.new_user_info["new_password"], "role",
                      self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                      self.new_user_info["new_phone"], self.new_user_info["new_address"]), "Allowed bad role")

        # bad number
        self.assertFalse(edit_user(self.user.user_id, self.new_user_info["new_password"], self.new_user_info["new_role"],
                      self.new_user_info["new_first_name"], self.new_user_info["new_last_name"],
                      "123-456-789", self.new_user_info["new_address"]), "ALlowed bad number")