from supercreative.models import (User, Course, Section)
from django.core.exceptions import ObjectDoesNotExist


def create_session(session, login_email):
    if not User.objects.filter(email=login_email).exists():
        print('user not found')
        return False

    user = User.objects.get(email=login_email)

    # only store the user_id and role in the session
    session["user_id"] = user.user_id
    session["role"] = user.role_id.role_name
    session.save()
    return True


def end_session(session):
    # session.items() isn't a standard dictionary, so I can't just pull a list of keys from it with session.keys().
    # I think there must be a better way to do it than looping through twice, but I couldn't find one.
    key_list = []
    for key, value in session.items():
        key_list.append(key)
    for key in key_list:
        try:
            del session[key]
        except TypeError:
            pass
    session.save()


def active_session_exists(request):
    try:
        active_user = User.objects.get(user_id=request.session['user_id'])
    except KeyError:
        return False

    if active_user.role_id.role_name != request.session['role']:
        return False
    else:
        return True


def did_logout(request):
    end_session(request.session)
    for key in request.session.items():
        return False
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
