def logout(session):
    key_list = []
    for key, value in session.items():
        key_list.append(key)
    for key in key_list:
        try:
            del session[key]
        except TypeError:
            pass
    session.save()