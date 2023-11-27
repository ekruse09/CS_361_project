from supercreative.models import User


def active_session_exists(request):
    try:
        active_user = User.objects.get(user_id=request.session['user_id'])
    except KeyError:
        return False

    if active_user.role != request.session['role']:
        return False
    else:
        return True
