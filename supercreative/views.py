from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.views import View
from supercreative.course.user_assignments import assign_user_to
from supercreative.section import section as section_helper
from supercreative.course import course as courseHelper
from supercreative.user import user as userHelper
from supercreative.models import User, Course, Section, UserCourseAssignment, SectionType
from supercreative.authentication import authentication


class Login(View):
    def get(self, request):
        if authentication.did_logout(request) is True:
            return render(request, 'login.html', {})
        else:
            return redirect("/")

    def post(self, request):
        if authentication.did_login(request) is False:
            return render(request, 'login.html',
                          {'message': "No account found with that email and password"})
        else:
            return redirect("home/")


class Test(View):
    def get(self, request):
        if authentication.active_session_exists(request):
            return render(request, 'test_page.html',
                          {'user_id': request.session['user_id'], 'role': request.session['role']})
        else:
            return redirect("/")
        # return render(request, 'test_page.html')


class Home(View):
    def get(self, request):
        if authentication.active_session_exists(request):
            name = User.objects.get(user_id=request.session['user_id']).first_name
            return render(request, 'index.html',
                          {'first_name': name, 'user_id': request.session['user_id'],
                           'role': request.session['role']})
        else:
            return redirect("/")


class Users(View):
    def get(self, request):
        if not authentication.active_session_exists(request):
            return redirect("/")
        role = request.session['role']
        # get all the users
        users = User.objects.all()
        return render(request, 'users.html',
                      {'users': users,
                                'role': role})

    def post(self, request):
        if not authentication.active_session_exists(request):
            return redirect("/")

        users = User.objects.all()
        role = request.session['role']

        if 'view_user' in request.POST.get('action'):
            user_id = request.POST.get('user_id')
            user = User.objects.get(user_id=user_id)
            return render(request,
                          'users.html',
                          {'users': users,
                                   'user': user,
                                   'popup': True,
                                   'edit': False,
                                   'new': False,
                                   'role': role})

        elif 'request_edit' in request.POST.get('action'):
            user_id = request.POST.get('user_id')
            user = User.objects.get(user_id=user_id)
            return render(request, 'users.html',
                          {'users': users,
                                   'user': user,
                                   'popup': True,
                                   'edit': True,
                                   'new': False,
                                   'role': role})

        elif 'request_new' in request.POST.get('action'):
            return render(request, 'users.html',
                          {'users': users,
                           'popup': True,
                           'edit': True,
                           'new': True,
                           'role': role})

        elif 'new_user' in request.POST.get('action'):
            # localize variables
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            response = userHelper.create_user(email,
                                              password,
                                              role,
                                              first_name,
                                              last_name,
                                              phone_number,
                                              address)

            return render(request, 'users.html',
                          {'users': users,
                                   'popup': True,
                                   'edit': True,
                                   'new': True,
                                   'error': response,
                                   'role': role})

        elif 'edit_user' in request.POST.get('action'):
            # localize variables
            user_id = int(request.POST.get('user_id'))
            password = request.POST.get('password')
            role = request.POST.get('role')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            response = userHelper.edit_user(user_id,
                                            password,
                                            role,
                                            first_name,
                                            last_name,
                                            phone_number,
                                            address)

            return render(request, 'users.html',
                          {'users': users,
                                   'popup': True,
                                   'edit': True,
                                   'new': False,
                                   'error': response,
                                   'role': role})

        elif 'delete_user' in request.POST.get('action'):
            userHelper.delete_user(request.POST.get('user_id'))
            return render(request, 'users.html', {'users': users, 'role': role})

        else:
            return render(request, 'users.html', {'users': users, 'role': role})


class Courses(View):
    def get(self, request):
        role = request.session['role']
        if not authentication.active_session_exists(request):
            return redirect("/")
        # get all the courses
        courses = Course.objects.all()
        return render(request, 'courses.html', {'courses': courses, 'role': role})

    def post(self, request):
        role = request.session['role']
        if not authentication.active_session_exists(request):
            return redirect("/")

        courses = Course.objects.all()

        if 'view_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'courses.html',
                          {'courses': courses,
                                   'course': course,
                                   'popup': True,
                                   'edit': False,
                                   'role': role,
                                   'new': False})

        elif 'request_edit' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'courses.html',
                          {'courses': courses,
                                   'course': course,
                                   'popup': True,
                                   'edit': True,
                                   'new': False,
                                   'role': role})

        elif 'request_new' in request.POST.get('action'):
            return render(request, 'courses.html',
                                  {'courses': courses,
                                   'popup': True,
                                   'edit': True,
                                   'new': True,
                                   'role': role})

        elif 'new_course' in request.POST.get('action'):
            # localize variables
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')

            response = courseHelper.create_course(course_name, course_description, course_code)
            return render(request,
                          'courses.html',
                          {'courses': courses,
                           'popup': True,
                           'edit': True,
                           'new': True,
                           'error': response,
                           'role': role})

        elif 'edit_course' in request.POST.get('action'):
            # localize variables
            course_id = int(request.POST.get('course_id'))
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')

            response = courseHelper.edit_course(course_id, course_name, course_description, course_code)
            return render(request, 'courses.html',
                          {'courses': courses,
                                   'popup': True,
                                   'edit': True,
                                   'new': False,
                                   'error': response,
                                   'role': role})

        elif 'delete_course' in request.POST.get('action'):
            if Course.objects.filter(course_id=request.POST.get('course_id')):
                courseHelper.delete_course(Course.objects.get(course_id=request.POST.get('course_id')))
                return render(request, 'courses.html', {'courses': courses})
            else:
                return render(request, 'courses.html',
                              {'courses': courses,
                                       'popup': True,
                                       'edit': False,
                                       'new': False,
                                       'error': 'Course does not exist',
                                       'role': role})


        elif 'manage_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'manage-course.html', {'course': course,'role': role})

        return render(request, 'courses.html', {'courses': courses, 'role': role})


class ManageCourse(View):
    def get(self, request):
        # Check if an active session exists
        if not authentication.active_session_exists(request):
            return redirect("/")

        # Retrieve the course, its sections, and its assigned users
        course_id = request.POST.get('course_id')
        course = Course.objects.get(course_id=course_id)
        user_assignments = UserCourseAssignment.objects.filter(course_id=course_id)
        course_sections = Section.objects.filter(course_id=course_id)

        # Pass the sections as a dictionary with the user course assignments corresponding to that section
        uca_sections = {}
        for section in course_sections:
            current_uca = None
            try:
                current_uca = user_assignments.get(course_id=course_id,section_id=section)
            except ObjectDoesNotExist:
                current_uca = ""
            uca_sections[section] = current_uca

        return render(request,
                      'manage-course.html',
                      {'course': course_id,
                       'uca_sections': uca_sections,
                       'role': request.session['role']})

    def post(self, request):
        # Check if an active session exists
        if not authentication.active_session_exists(request):
            return redirect("/")

        # Retrieve the course, its sections, and its assigned users
        course_id = request.POST.get('course_id')
        course = Course.objects.get(course_id=course_id)
        user_assignments = UserCourseAssignment.objects.filter(course_id=course_id)
        course_sections = Section.objects.filter(course_id=course)

        # Pass the sections as a dictionary with the user course assignments corresponding to that section
        uca_sections = {}
        for section in course_sections:
            current_uca = None
            try:
                current_uca = user_assignments.get(course_id=course_id, section_id=section)
            except ObjectDoesNotExist:
                current_uca = ""
            uca_sections[section] = current_uca

        # Handle user course assignment and (optional) section assignment
        if 'assign_user' in request.POST.get('action'):
            user_id = request.POST.get('user_id')

            section_id = request.POST.get('section_id')

            # Assign the user to the course
            response = assign_user_to(assigned_user=User.objects.get(user_id=user_id),
                                      assigned_course=Course.objects.get(course_id=course_id),
                                      assigned_section=section_id)
            return render(request,
                          'manage-course.html',
                          {'course': course,
                           'uca_sections': uca_sections,
                           'error': response,
                           'role': request.session['role']})

        # Loads the popup for a new section
        elif 'request_new' in request.POST.get('action'):

            # list of users assigned to the course
            assigned_users = User.objects.filter(user_id__in=user_assignments.values_list('user_id'))

            return render(request, 'manage-course.html',
                          {'course': course,
                           'assigned_users': assigned_users,
                           'section_types': SectionType.objects.all(),
                           'popup': True,
                           'edit': True,
                           'new': True,
                           'role': request.session['role']})


class UserPage(View):
    def get(self, request):
        if not authentication.active_session_exists(request):
            return redirect("/")
        # get the user signed in on this session
        user = User.objects.get(user_id=request.session['user_id'])
        return render(request, 'users.html', {'user': user})

    def post(self, request):
        user = User.objects.get(user_id=request.session['user_id'])
        if not authentication.active_session_exists(request):
            return redirect("/")

        elif 'edit_user' in request.POST.get('action'):

            # localize variables
            user_id = int(request.POST.get('user_id'))
            password = request.POST.get('password')
            role = request.POST.get('role')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            skills = request.POST.get('skills')

            response = userHelper.edit_user_with_skills(user_id,
                                            password,
                                            role,
                                            first_name,
                                            last_name,
                                            phone_number,
                                            address,
                                            skills)
            print(response)
            return render(request, 'users.html',
                          {'user': user, 'popup': True, 'edit': True, 'new': False, 'error': response})






















































