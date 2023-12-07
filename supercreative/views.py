from django.shortcuts import redirect, render
from django.views import View
from supercreative.course import course as courseHelper
from supercreative.course.assign_user import assign_user_to
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
            userHelper.create_user(int(request.POST.get('user_id')), request.POST.get('email'),
                                   request.POST.get('password'), request.POST.get('role'),
                                   request.POST.get('first_name'), request.POST.get('last_name'),
                                   request.POST.get('phone_number'), request.POST.get('address'))
            return render(request, 'users.html', {'users': users})

        elif 'edit_user' in request.POST.get('action'):
            userHelper.edit_user(int(request.POST.get('user_id')), request.POST.get('password'),
                                 request.POST.get('role'), request.POST.get('first_name'),
                                 request.POST.get('last_name'), request.POST.get('phone_number'),
                                 request.POST.get('address'))
            return render(request, 'users.html', {'users': users})

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
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')

            if courseHelper.course_id_to_int(course_id) is None:
                return render(request, 'courses.html',
                              {'courses': courses, 'popup': True, 'edit': True, 'new': True,
                               'error': 'course ID must be an integer'})

            response = courseHelper.create_course(int(course_id), course_name, course_description, course_code)
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

            if courseHelper.course_id_to_int(course_id) is None:
                return render(request, 'courses.html',
                              {'courses': courses, 'popup': True, 'edit': True, 'new': False,
                               'error': 'course ID must be an integer'})

            if courseHelper.edit_course(course_id, course_name, course_description, course_code) is False:
                return render(request, 'courses.html',
                              {'courses': courses, 'popup': True, 'edit': True, 'new': False,
                               'error': 'Some of the course information you entered is invalid please review'})

            return render(request, 'courses.html', {'courses': courses})

        elif 'delete_course' in request.POST.get('action'):
            if Course.objects.filter(course_id=request.POST.get('course_id')):
                courseHelper.delete_course(Course.objects.get(course_id=request.POST.get('course_id')))
                return render(request, 'courses.html', {'courses': courses})
            else:
                return render(request, 'courses.html',
                              {'courses': courses, 'popup': True, 'edit': False, 'new': False,
                               'error': 'course does not exist'})

        return render(request, 'courses.html', {'courses': courses})


class ManageCourses(View):
    def get(self, request, course_id):
        # Check if an active session exists
        if not authentication.active_session_exists(request):
            return redirect("/")

        try:
            # Retrieve the course and its assigned users
            course = Course.objects.get(course_id=course_id)
            assigned_users = UserCourseAssignment.objects.filter(course_id=course_id)

            return render(request, 'manage_courses.html', {'course': course, 'assigned_users': assigned_users})

        except Course.DoesNotExist:
            return render(request, 'manage_courses.html', {'error': 'Course not found'})

    def post(self, request, course_id):
        # Check if an active session exists
        if not authentication.active_session_exists(request):
            return redirect("/")

        try:
            # Retrieve the course
            course = Course.objects.get(course_id=course_id)

            # Handle user course assignment and (optional) section assignment
            if 'assign_user' in request.POST.get('action'):
                user_id = request.POST.get('user_id')
                if 'section_id' in request.POST:
                    section_id = request.POST.get('section_id')
                else:
                    section_id = None

                # Check if the user is already assigned to the course and section (optional)
                if UserCourseAssignment.objects.filter(user_id=user_id, course_id=course_id,
                                                       section_id=section_id).exists():
                    return render(request, 'manage_courses.html', {'course': course,
                                                                   'error': 'User is already assigned to the course '
                                                                            'and section'})
                # Assign the user to the course
                assign_user_to(assigned_user=user_id, assigned_course=course_id, assigned_section=section_id)

                # Retrieve the updated list of assigned users
                assigned_users = UserCourseAssignment.objects.filter(course_id=course_id)

                return render(request, 'manage_courses.html', {'course': course, 'assigned_users': assigned_users})

        except Course.DoesNotExist:
            return render(request, 'manage_courses.html', {'error': 'Course not found'})
