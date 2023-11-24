from supercreative.models import (User, Course, Section)


def create_session(session, email):
    user = User.objects.get(email)

    if user is None:
        return False

    session["user_id"] = user.user_id
    session["role"] = user.role
    session.save()

    return True
