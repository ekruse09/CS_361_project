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
