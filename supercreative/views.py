from django.shortcuts import redirect,render
from django.views import View
from supercreative.authentication import authentication


class Login(View):
    def get(self, request):
        if logout.did_logout(request) is True:
            return render(request, 'login.html', {})
        else:
            return redirect("/")

    def post(self, request):
        if login.did_login(request) is False:
            return render(request, 'login.html',
                          {'message':"No account found with that email and password"})
        else:
            return redirect("test/")

class Test(View):
    def get(self, request):
        if authentication.active_session_exists(request):
            return render(request, 'test_page.html',
                          {'user_id': request.session['user_id'], 'role': request.session['role']})
        else:
            return redirect("/")
        return render(request, 'test_page.html')

class Course(View):
    def get(self, request):
        #get all the courses
        courses = Course.objects.all()
        return render(request, 'course.html', {'courses': courses})

    def post(self, request):

        if 'new_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')
            course.create_course(course_id, course_name, course_description, course_code)
            return redirect('/course')

        elif 'select_edit' in request.POST.get('action'):
            return redie

        elif 'edit_cousre' in request.POST.get('action'):
            if not course.check_existence(request.POST.get('course_id')):
                return course.nonexistense_error()
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')
            course.edit_course(course_id, course_name, course_description, course_code)
            return redirect('/course')

        elif 'delete_course' in request.POST.get('action'):
            if not course.check_existence(request.POST.get('course_id')):
                return course.nonexistense_error()
            course_id = request.POST.get('course_id')
            course.delete_course(course_id)
            return redirect('/course')

        else:
            return redirect('/course')
        return render(request, 'test_page.html', {'user_id':request.session['user_id'], 'role':request.session['role']})





