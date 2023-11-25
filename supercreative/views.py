from django.shortcuts import redirect,render
from django.views import View
from supercreative.Logout.logout import end_session
def logout(request):
    end_session(request.session)
    return redirect('/')

class Login(View):
    def get(self, request):
        logout(request)
        return render(request, 'login.html', {})

    def post(self, request):
        return redirect('/test')
class Test(View):
    def get(self, request):
        return render(request, 'test_page.html')
