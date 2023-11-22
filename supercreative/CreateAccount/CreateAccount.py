import string
from supercreative.models import User


def create_user(uid, email, password, role, first, last, phone, address):
    if not isinstance(uid, int) and User.objects.filter(user_id=uid).exists() or uid <= 0:
        return False

    if not isinstance(email, str) and User.objects.filter(email=email).exists() or len(email) == 0:
        return False

    hold = email
    if '@' in hold:
        site = hold.partition('@')
        if site[2] != 'uwm.edu':
            return False
    else:
        return False

    if not isinstance(password, str) or len(password) == 0:
        return False

    upper = any(i.isupper() for i in User.objects.get(user_id=1).password)
    lower = any(i.islower() for i in User.objects.get(user_id=1).password)
    special = any(i in string.punctuation for i in User.objects.get(user_id=1).password)

    if not upper or not lower or not special:
        return False

    if not isinstance(role, str) or len(role) == 0:
        return False

    if not isinstance(first, str) or len(first) == 0:
        return False

    if not isinstance(last, str) or len(last) == 0:
        return False

    if not isinstance(phone, str) or len(phone) == 0:
        return False

    if not isinstance(address, str) or len(address) == 0:
        return False

    new_user = User(user_id=uid, email=email, password=password, role=role, first_name=first, last_name=last,
                    phone_number=phone, address=address)
    new_user.save()

    return True
