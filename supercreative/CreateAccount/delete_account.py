from supercreative.models import User, UserCourseAssignment
from django.core.exceptions import ObjectDoesNotExist


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
