from django.test import TestCase, Client
from supercreative.course import course
from supercreative.section import section
from supercreative.course import user_assignments
from supercreative.models import Course, UserCourseAssignment, Section, SectionType, UserRole, User
from supercreative.authentication import authentication
from supercreative.user import user


class ManageCoursesAcceptanceTests(TestCase):
    client = None
    existing_course = None
    existing_section_1 = None
    existing_section_2 = None
    existing_user_1 = None
    existing_user_2 = None
    existing_user_3 = None
    expected_uca = None

    def setUp(self):
        self.client = Client()

        # Set up data for the whole TestCase

        # Set up course
        self.course_code = 'TC101'
        course.create_course(name='Test course',
                             description='Test Description',
                             code=self.course_code)
        self.existing_course = Course.objects.get(course_code=self.course_code)

        # Set up user
        self.role_1 = UserRole.objects.create(role_name="Instructor")
        self.email_1 = 'test@uwm.edu'
        user.create_user(email=self.email_1,
                         password='P@ssword123',
                         role=self.role_1.role_name,
                         first='Jayson',
                         last='Rock',
                         phone='1234567890',
                         address='123 Sesame St')
        self.existing_user_1 = User.objects.get(email=self.email_1)

        # Set up 2nd user
        self.role_2 = UserRole.objects.create(role_name="TA")
        self.email_2 = 'user2@uwm.edu'
        user.create_user(email=self.email_2,
                         password='uSer1!23',
                         role=self.role_2.role_name,
                         first='New',
                         last='User',
                         phone='1234567491',
                         address='321 Sesame St')
        self.existing_user_2 = User.objects.get(email=self.email_2)

        # Set up 3rd user
        self.role_3 = UserRole.objects.create(role_name="Administrator")
        self.email_3 = 'user@uwm.edu'
        user.create_user(email=self.email_3,
                         password='u1E#23',
                         role=self.role_3.role_name,
                         first='User',
                         last='New',
                         phone='1244567891',
                         address='212 Sesame St')
        self.existing_user_3 = User.objects.get(email=self.email_3)

        # Set up section
        section_type_1 = SectionType.objects.create(section_type_name="discussion")
        section.create_section(course=self.existing_course,
                               section_type=section_type_1.section_type_name)

        # Set up section 2nd section
        section_type_2 = SectionType.objects.create(section_type_name="LAB")
        section.create_section(course=self.existing_course,
                               section_type=section_type_2.section_type_name)

        # Get the sections
        section_objects = Section.objects.all()
        self.existing_section_1 = section_objects[0]
        self.existing_section_2 = section_objects[1]

        # assign user #1 to section #2
        user_assignments.assign_user_to(assigned_course=self.existing_course,
                                        assigned_section=self.existing_section_2,
                                        assigned_user=self.existing_user_1)

        # assign user #2 to just the course
        user_assignments.assign_user_to(assigned_course=self.existing_course,
                                        assigned_user=self.existing_user_2)

        # make the expected user course assignment/section dictionary
        self.expected_uca = {self.existing_section_1: "",
                             self.existing_section_2: UserCourseAssignment.objects.get(
                                 section_id=self.existing_section_2)}

        authentication.create_session(self.client.session, self.existing_user_1.email)

    def test_get_manage_course(self):
        response = self.client.get('/manage-course/', {'course_id': self.existing_course.course_id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)

        self.assertIn('uca_sections', response.context)

        # Add assertions for the expected values in the uca_sections dictionary
        uca_sections = response.context['uca_sections']
        expected_uca = self.expected_uca
        self.assertIsInstance(uca_sections, dict)
        for current_section in uca_sections:
            self.assertEqual(uca_sections[current_section],
                             expected_uca[current_section])

    def test_post_assign_user_to_course(self):
        response = self.client.post('/manage-course/',
                                    {'action': 'assign_user',
                                     'user_id': self.existing_user_3.user_id,
                                     'course_id': self.existing_course.course_id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('uca_sections', response.context)

        # make sure the user assignment was created
        self.assertTrue( UserCourseAssignment.objects.filter(user_id=self.existing_user_3).exists())

        # Add assertions for the expected values in the uca_sections dictionary
        uca_sections = response.context['uca_sections']
        expected_uca = self.expected_uca
        self.assertIsInstance(uca_sections, dict)

        for current_section in uca_sections:
            self.assertEqual(uca_sections[current_section],
                             expected_uca[current_section])

    def test_post_request_new_section(self):
        response = self.client.post('/manage-course/',
                                    {'action': 'request_new',
                                     'course_id': self.existing_course.course_id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('assigned_users', response.context)
        self.assertIn('section_types', response.context)
        self.assertTrue(response.context['popup'])
        self.assertTrue(response.context['edit'])
        self.assertTrue(response.context['new'])

    def test_post_new_section(self):
        response = self.client.post('/manage-course/',
                                    {'action': 'new_section',
                                     'course_id': self.existing_course.course_id,
                                     'section_type': self.existing_section_2.section_type.section_type_name})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('uca_sections', response.context)

        # Add assertions for the expected values in the uca_sections dictionary
        print(Section.objects.all())
        self.assertTrue(Section.objects.filter(section_id=2).exists())

    def test_post_delete_section(self):
        response = self.client.post('/manage-course/',
                                    {'action': 'delete_section',
                                     'section_id': self.existing_section_2.section_id,
                                     'course_id': self.existing_course.course_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('uca_sections', response.context)
        # Add assertions for the expected values in the uca_sections dictionary
        self.assertFalse(Section.objects.filter(course_id=self.existing_section_2.course_id, section_id=self.existing_section_2.section_id), "Failed to delete section.")

        # Check to see if user assignment is gone
        self.assertFalse(UserCourseAssignment.objects.filter(section_id=self.existing_section_2).exists())

    def test_post_invalid_action(self):
        response = self.client.post('/manage-course/', {'action': 'invalid_action', 'course_id':self.existing_course.course_id})

        self.assertEqual(response.status_code, 200)  # Should return a response even for an invalid action

    def test_post_add_user(self):
        response = self.client.post('/manage-course/',
                                    {'action': 'add_user',
                                     'course_id': self.existing_course.course_id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')

        self.assertIn('course', response.context)
        self.assertIn('eligible_users', response.context)
        self.assertTrue(response.context['add_user'])

        # user 3 is the only user not assigned to the course
        eligible_users = response.context['eligible_users']
        self.assertTrue(self.existing_user_3 in eligible_users)

    def test_post_view_section(self):
        response = self.client.post('/manage-course/',
                                    {'action': 'view_section',
                                     'section_id': self.existing_section_2.section_id,
                                     'course_id': self.existing_course.course_id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-course.html')
        self.assertIn('course', response.context)
        self.assertIn('uca_sections', response.context)
        self.assertTrue(response.context['popup'])

        # Add assertions for the expected values in the uca_sections dictionary
        uca_sections = response.context['uca_sections']
        expected_uca = self.expected_uca
        self.assertIsInstance(uca_sections, dict)

        for current_section in uca_sections:
            self.assertEqual(first=uca_sections[current_section],
                             second=expected_uca[current_section])
