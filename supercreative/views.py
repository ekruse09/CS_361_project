from django.shortcuts import redirect, render
from django.views import View
from supercreative.course import course as courseHelper
from supercreative.course.assign_user import assign_user_to
from supercreative.create_sections import section as section_helper
from supercreative.user import user as userHelper
from supercreative.models import User, Course, Section, UserCourseAssignment
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
        # get all the users
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})

    def post(self, request):
        if not authentication.active_session_exists(request):
            return redirect("/")

        users = User.objects.all()

        if 'view_user' in request.POST.get('action'):
            user_id = request.POST.get('user_id')
            user = User.objects.get(user_id=user_id)
            return render(request, 'users.html',
                          {'users': users, 'user': user, 'popup': True, 'edit': False})

        elif 'request_edit' in request.POST.get('action'):
            user_id = request.POST.get('user_id')
            user = User.objects.get(user_id=user_id)
            return render(request, 'users.html',
                          {'users': users, 'user': user, 'popup': True, 'edit': True, 'new': False})

        elif 'request_new' in request.POST.get('action'):
            return render(request, 'users.html',
                          {'users': users, 'popup': True, 'edit': True, 'new': True})

        elif 'new_user' in request.POST.get('action'):
            # localize variables
            user_id = int(request.POST.get('user_id'))
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')

            response = userHelper.create_user(user_id,
                                              email,
                                              password,
                                              role,
                                              first_name,
                                              last_name,
                                              phone_number,
                                              address)

            return render(request, 'users.html',
                          {'users': users, 'popup': True, 'edit': True, 'new': True, 'error': response})

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
                          {'users': users, 'popup': True, 'edit': True, 'new': False, 'error': response})

        elif 'delete_user' in request.POST.get('action'):
            userHelper.delete_user(request.POST.get('user_id'))
            return render(request, 'users.html', {'users': users})

        else:
            return render(request, 'users.html', {'users': users})


class Courses(View):
    def get(self, request):
        if not authentication.active_session_exists(request):
            return redirect("/")
        # get all the courses
        courses = Course.objects.all()
        return render(request, 'courses.html', {'courses': courses})

    def post(self, request):
        if not authentication.active_session_exists(request):
            return redirect("/")

        courses = Course.objects.all()

        if 'view_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'courses.html',
                          {'courses': courses, 'course': course, 'popup': True, 'edit': False})

        elif 'request_edit' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'courses.html',
                          {'courses': courses, 'course': course, 'popup': True, 'edit': True, 'new': False})

        elif 'request_new' in request.POST.get('action'):
            return render(request, 'courses.html',
                          {'courses': courses, 'popup': True, 'edit': True, 'new': True})

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
                           'error': response})

        elif 'edit_course' in request.POST.get('action'):
            # localize variables
            course_id = int(request.POST.get('course_id'))
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')

            response = courseHelper.edit_course(course_id, course_name, course_description, course_code)
            return render(request, 'courses.html',
                          {'courses': courses, 'popup': True, 'edit': True, 'new': False,
                           'error': response})

        elif 'delete_course' in request.POST.get('action'):
            if Course.objects.filter(course_id=request.POST.get('course_id')):
                courseHelper.delete_course(Course.objects.get(course_id=request.POST.get('course_id')))
                return render(request, 'courses.html', {'courses': courses})
            else:
                return render(request, 'courses.html',
                              {'courses': courses, 'popup': True, 'edit': False, 'new': False,
                               'error': 'course does not exist'})

        elif 'manage_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'manage-course.html', {'course': course})

        return render(request, 'courses.html', {'courses': courses})


class ManageCourse(View):
    def get(self, request):
        # Check if an active session exists
        if not authentication.active_session_exists(request):
            return redirect("/")

        # Retrieve the course and its assigned users
        course_id = request.POST.get('course_id')
        course = Course.objects.get(course_id=course_id)
        assigned_users = UserCourseAssignment.objects.filter(course_id=course_id)

        return render(request,
                      'manage-courses.html',
                      {'course': course,
                       'assigned_users': assigned_users})

    def post(self, request):
        # Check if an active session exists
        if not authentication.active_session_exists(request):
            return redirect("/")

        # Retrieve the course
        course_id = request.POST.get('course_id')
        course = Course.objects.get(course_id=course_id)

        # Retrieve the assigned users
        user_assignments = UserCourseAssignment.objects.filter(course_id=course_id)

        # Handle user course assignment and (optional) section assignment
        if 'assign_user' in request.POST.get('action'):
            user_id = request.POST.get('user_id')

            # Assign the user to the course
            response = assign_user_to(assigned_user=user_id, assigned_course=course_id)

            # Retrieve the updated list of assigned users
            user_assignments = UserCourseAssignment.objects.filter(course_id=course_id)

            return render(request,
                          'manage-course.html',
                          {'course': course,
                           'user_assignments': user_assignments,
                           'error': response})

        elif 'request_new' in request.POST.get('action'):

            assigned_users = User.objects.filter(user_id__in=user_assignments.values_list('user_id'))

            return render(request, 'manage-course.html',
                          {'course': course,
                           'assigned_users': assigned_users,
                           'popup': True,
                           'edit': True,
                           'new': True})

        elif 'new_section' in request.POST.get('action'):
            # Localize variables
            section_id = request.POST.get('section_id')
            section_type = request.POST.get('section_type')
            user = request.POST.get('user')

            response = section_helper.create_section(section_id, course, section_type, user)

            # Get updated list of assigned users
            user_assignments = UserCourseAssignment.objects.filter(course_id=course_id)

            return render(request,
                          'manage-course.html',
                          {'course': course,
                           'user_assignments': user_assignments,
                           'popup': True,
                           'edit': True,
                           'new': True,
                           'error': response})

        elif 'delete_section' in request.POST.get('action'):
            # Localize variables
            section_id = request.POST.get('section_id')

            response = section_helper.delete_section(section_id)

            # Get updated list of assigned users
            user_assignments = UserCourseAssignment.objects.filter(course_id=course_id)

            return render(request,
                          'courses.html',
                          {'course': course,
                           'user_assignments': user_assignments,
                           'popup': True,
                           'edit': True,
                           'new': False,
                           'error': response})

        elif 'view_section' in request.POST.get('action'):

            return render(request, 'courses.html',
                          {'course': course,
                           'user_assignments': user_assignments,
                           'popup': True,
                           'edit': False})

        elif 'add_user' in request.POST.get('action'):

            all_users = User.objects.all()
            eligible_users = all_users.exclude(user_id__in=user_assignments.values_list('user_id'))

            return render(request, 'courses.html',
                          {'course': course,
                           'eligible_users': eligible_users,
                           'popup': True,
                           'edit': False})
