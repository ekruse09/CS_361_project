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
