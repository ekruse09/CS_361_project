from django.shortcuts import redirect,render
from django.views import View
from supercreative.Logout.logout import end_session
from supercreative.models import User, Course, Section, UserCourseAssignment
from supercreative.Course.course import create_course, edit_course, delete_course
def logout(request):
    end_session(request.session)
    return redirect('/')

class Login(View):
    def get(self,request):
        logout(request)
        return render(request, 'login.html', {})

    def post(self, request):
        return redirect('/test')
class Test(View):
    def get(self, request):
        return render(request, 'test_page.html')

class Course(View):
    def get(self, request):
        return render(request, 'course.html')

    def post(self, request):
        if request.method == 'POST':
            if 'new_user' in request.POST.get('action'):
                course_id = request.POST.get('course_id')
                course_name = request.POST.get('course_name')
                course_description = request.POST.get('course_description')
                course_code = request.POST.get('course_code')
                create_course(course_id, course_name, course_description, course_code)
                return redirect('/course')
            elif 'edit_user' in request.POST.get('action'):
                course_id = request.POST.get('course_id')
                course_name = request.POST.get('course_name')
                course_description = request.POST.get('course_description')
                course_code = request.POST.get('course_code')
                edit_course(course_id, course_name, course_description, course_code)
                return redirect('/course')
            elif 'delete_user' in request.POST.get('action'):
                course_id = request.POST.get('course_id')
                delete_course(course_id)
                return redirect('/course')
            else:
                return redirect('/course')



