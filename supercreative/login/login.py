from supercreative.models import (User, Course, Section)
from django.core.exceptions import ObjectDoesNotExist


def create_session(session, login_email):
    try:
        user = User.objects.get(email=login_email)

    except ObjectDoesNotExist:
        return False

    # only store the user_id and role in the session
    session["user_id"] = user.user_id
    session["role"] = user.role
    session.save()
    return True


def did_login(request):
    no_such_user = False
    bad_password = False
    try:
        m = User.objects.get(email=request.POST['email'])
        bad_password = (m.password != request.POST['password'])
    except:
        no_such_user = True
    if no_such_user or bad_password:
        return False
    else:
        create_session(request.session, request.POST['email'])
        return True
