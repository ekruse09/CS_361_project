from django.shortcuts import redirect,render
from django.views import View
from supercreative.Logout.logout import end_session
def logout(request):
    end_session(request.session)
    return redirect('/login')

class Login(View):
    def get(self,request):
        request.session['user_id'] = 1
        try:
            print(request.session['user_id'])
        except KeyError:
            pass
        end_session(request.session)
        try:
            print(request.session['user_id'])
        except KeyError:
            print("Session cleared")
        return render(request,'login.html',{})

    def post(self, request):
        return redirect('/')
class Test(View):
    def get(self, request):
        return render(request, 'test_page.html')
