import string
from supercreative.models import User, UserCourseAssignment
from django.core.exceptions import ObjectDoesNotExist


def create_user(uid, email, password, role, first, last, phone, address):
    if not isinstance(uid, int) or uid < 0:
        return "User ID must be a positive integer."
    elif User.objects.filter(user_id=uid).exists():
        return "User ID already exists."

    if len(email) == 0 or (not isinstance(email, str) or User.objects.filter(email=email).exists()):
        return "Email must be a unique string."

    hold = email
    if '@' in hold:
        site = hold.partition('@')
        if site[2] != 'uwm.edu':
            return "Email must be a uwm.edu address."
    else:
        return "email must contain an @ symbol."

    if len(password) == 0 or not isinstance(password, str):
        return "Password must be a string and non-empty."

    upper = any(i.isupper() for i in password)
    lower = any(i.islower() for i in password)
    special = any(i in string.punctuation for i in password)

    if not upper or not lower or not special:
        return "Password must contain at least one uppercase letter, one lowercase letter, and one special character."

    if len(role) == 0 or not isinstance(role, str):
        return "Role must be a string and non-empty."

    role.capitalize()
    valid_roles = ["ADMINISTRATOR", "INSTRUCTOR", "TA"]
    if role not in valid_roles:
        return "Role must be one of the following: ADMINISTRATOR, INSTRUCTOR, TA."

    if len(first) == 0 or not isinstance(first, str):
        return "First name must be a string and non-empty."

    if len(last) == 0 or not isinstance(last, str):
        return "Last name must be a string and non-empty."

    if len(phone) == 0 or not isinstance(phone, str):
        return "Phone number must be a string and non-empty."

    clean_phone = ''

    for char in phone:
        if char.isdigit():
            clean_phone += char

    if len(clean_phone) != 10:
        return "Phone number must be 10 digits."

    if not isinstance(address, str) or len(address) == 0:
        return "Address must be a string and non-empty."

    new_user = User(user_id=uid, email=email, password=password, role=role, first_name=first, last_name=last,
                    phone_number=clean_phone, address=address)
    new_user.save()

    return "User created successfully."


def edit_user(user_id, new_password, new_role, new_first, new_last, new_phone, new_address):
    if not User.objects.filter(user_id=user_id).exists():
        return False

    user = User.objects.get(user_id=user_id)
    print(user)

    if (new_password != '' and (any(i.isupper() for i in new_password)) and (any(i.islower() for i in new_password)) and
            (any(i in string.punctuation for i in new_password))):
        user.password = new_password
    else:
        return False

    new_role.upper()
    if new_role != '' and new_role in ["ADMINISTRATOR", "INSTRUCTOR", "TA"]:
        user.role = new_role
    else:
        return False

    if new_first != '':
        user.first_name = new_first
    else:
        return False

    if new_last != '':
        user.last_name = new_last
    else:
        return False

    clean_phone = ''
    for char in new_phone:
        if char.isdigit():
            clean_phone += char

    if len(clean_phone) == 10:
        user.phone_number = new_phone
    else:
        return False

    if new_address != '':
        user.address = new_address
    else:
        return False

    user.save()

    return True

def delete_user(user_id):
    # Preconditions

    try:
        # Check if the target userID exists in the Users table
        user = User.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return False

    # Postconditions
    # Remove all entries from the User-Course Assignments table that have the deleted UserID
    UserCourseAssignment.objects.filter(user_id=user).delete()

    # Delete the selected User account
    user.delete()

    # Return true if the selected User account was deleted
    return True