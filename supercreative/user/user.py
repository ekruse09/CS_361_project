import string
from supercreative.models import User, UserCourseAssignment, UserRole
from django.core.exceptions import ObjectDoesNotExist


def create_user(email, password, role, first, last, phone, address):
    if User.objects.filter(email=email).exists():
        return "Email already exists."
    elif len(email) == 0 or (not isinstance(email, str)):
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

    if not UserRole.objects.filter(role_name=role).exists():
        return "Invalid role selected."

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

    User.objects.create(email=email,
                        password=password,
                        role_id=UserRole.objects.get(role_name=role),
                        first_name=first,
                        last_name=last,
                        phone_number=clean_phone,
                        address=address)

    return "User created successfully."


def edit_user(user_id, new_password, new_role, new_first, new_last, new_phone, new_address):
    try:
        user = User.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return "User ID does not exist."

    if new_password != '' and (any(i.isupper() for i in new_password)) and (any(i.islower() for i in new_password)) and (any(i in string.punctuation for i in new_password)):
        user.password = new_password
    else:
        return "Password must contain at least one uppercase letter, one lowercase letter, and one special character."

    if UserRole.objects.filter(role_name=new_role).exists():
        user.role_id = UserRole.objects.get(role_name=new_role)
    else:
        return "Invalid role selected."

    if new_first != '':
        user.first_name = new_first
    else:
        return "First name must be a string and non-empty."

    if new_last != '':
        user.last_name = new_last
    else:
        return "Last name must be a string and non-empty."

    clean_phone = ''
    for char in new_phone:
        if char.isdigit():
            clean_phone += char

    if len(clean_phone) == 10:
        user.phone_number = new_phone
    else:
        return "Phone number must be 10 digits."

    if new_address != '':
        user.address = new_address
    else:
        return "Address must be a string and non-empty."

    user.save()

    return "User edited successfully."

def delete_user(user_id):
    # Preconditions

    try:
        # Check if the target userID exists in the Users table
        user = User.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return "User not found."

    # Postconditions
    # Remove all entries from the User-Course Assignments table that have the deleted UserID
    UserCourseAssignment.objects.filter(user_id=user).delete()

    # Delete the selected User account
    user.delete()

    # Return true if the selected User account was deleted
    return "Successfully deleted user."

def edit_user_with_skills(user_id, new_password, new_role, new_first, new_last, new_phone, new_address, skills):
    result = edit_user(user_id, new_password, new_role, new_first, new_last, new_phone, new_address)
    user = User.objects.get(user_id=user_id)
    user.skills = skills
    user.save()

    return result + " (with skills)"