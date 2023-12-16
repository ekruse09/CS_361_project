from django.shortcuts import redirect, render
from django.views import View
from supercreative.course import course as courseHelper
from supercreative.user import user as userHelper
from supercreative.models import User, Course
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
                           'error': response})

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

        return render(request, 'courses.html', {'courses': courses})
