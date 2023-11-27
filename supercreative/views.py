from django.shortcuts import redirect,render
from django.views import View
from supercreative.Logout.logout import end_session
from supercreative.models import User, Course, Section, UserCourseAssignment
import supercreative.Course.course as course
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

        if 'new_course' in request.POST.get('action'):
            course_id = request.POST.get('course_id')
            course_name = request.POST.get('course_name')
            course_description = request.POST.get('course_description')
            course_code = request.POST.get('course_code')
            course.create_course(course_id, course_name, course_description, course_code)
            return redirect('/course')

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



