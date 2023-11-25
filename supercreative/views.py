from django.shortcuts import redirect,render
from django.views import View
from supercreative.logout import logout
from supercreative.login import login
from supercreative.models import User

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
        return render(request, 'test_page.html', {'user_id':request.session['user_id'], 'role':request.session['role']})





