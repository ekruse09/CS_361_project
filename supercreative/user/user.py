import string
from supercreative.models import User


def create_user(uid, email, password, role, first, last, phone, address):
    if not isinstance(uid, int) or User.objects.filter(user_id=uid).exists() or uid <= 0:
        return False

    if len(email) == 0 or (not isinstance(email, str) or User.objects.filter(email=email).exists()):
        return False

    hold = email
    if '@' in hold:
        site = hold.partition('@')
        if site[2] != 'uwm.edu':
            return False
    else:
        return False

    if len(password) == 0 or not isinstance(password, str):
        return False

    upper = any(i.isupper() for i in password)
    lower = any(i.islower() for i in password)
    special = any(i in string.punctuation for i in password)

    if not upper or not lower or not special:
        return False

    if len(role) == 0 or not isinstance(role, str):
        return False

    role.capitalize()
    valid_roles = ["ADMINISTRATOR", "INSTRUCTOR", "TA"]
    if role not in valid_roles:
        return False

    if len(first) == 0 or not isinstance(first, str):
        return False

    if len(last) == 0 or not isinstance(last, str):
        return False

    if len(phone) == 0 or not isinstance(phone, str):
        return False

    clean_phone = ''

    for char in phone:
        if char.isdigit():
            clean_phone += char

    if len(clean_phone) != 10:
        return False

    if not isinstance(address, str) or len(address) == 0:
        return False

    new_user = User(user_id=uid, email=email, password=password, role=role, first_name=first, last_name=last,
                    phone_number=clean_phone, address=address)
    new_user.save()

    return True
