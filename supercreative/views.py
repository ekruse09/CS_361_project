from django.shortcuts import redirect,render
from django.views import View
from supercreative.Course import course_helper as courseHelper
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
                          {'message':"No account found with that email and password"})
        else:
            return redirect("course/")

class Test(View):
    def get(self, request):
        if authentication.active_session_exists(request):
            return render(request, 'test_page.html',
                          {'user_id': request.session['user_id'], 'role': request.session['role']})
        else:
            return redirect("/")
        return render(request, 'test_page.html')

class Courses(View):
    def get(self, request):
        #get all the courses
        courses = Course.objects.all()
        val = True
        return render(request, 'courses.html', {'courses': courses, 'pool': val})

    def post(self, request):

        if 'view_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'courses.html', {'course': course, 'popup': True, 'edit': False})

        elif 'request_edit' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            return render(request, 'courses.html', {'course': course, 'popup': True, 'edit': True})

        elif 'request_new' in request.POST.get('action'):
            return render(request, 'courses.html', {'popup': True, 'edit': True})

        if 'new_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')
            courseHelper.create_course(course_id, course_name, course_description, course_code)
            return redirect(request.path)

        elif 'edit_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course = Course.objects.get(course_id=course_id)
            course_name = course.course_name
            course_description = course.course_description
            course_code = course.course_code
            courseHelper.edit_course(course_id, course_name, course_description, course_code)
            return redirect(request.path)

        elif 'delete_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            courseHelper.delete_course(course_id)
            return redirect(request.path)

        else:
            return redirect('course/')




