from supercreative.models import Course, Section, UserCourseAssignment, SectionType, User
from django.core.exceptions import ObjectDoesNotExist


# section assignment not implemented until sprint 2
def assign_user_to(assigned_user, assigned_course, assigned_section=None):
    if not isinstance(assigned_course, Course):
        return "invalid course input"

    if assigned_section is None:
        if UserCourseAssignment.objects.filter(user_id=assigned_user,
                                               course_id=assigned_course,
                                               section_id=None).exists():
            return "assignment already exists"
        UserCourseAssignment.objects.create(user_id=assigned_user,
                                            course_id=assigned_course,
                                            section_id=None,
                                            section_type=None)
    else:
        # Check if user has already been assigned to the course and section
        if UserCourseAssignment.objects.filter(user_id=assigned_user,
                                               course_id=assigned_course,
                                               section_id=assigned_section).exists():

            return "assignment already exists"
        # Find existing assignment for the Course and Section
        else:
            updated_assignment = None
            try:
                updated_assignment = UserCourseAssignment.objects.get(course_id=assigned_course,
                                                                      section_id=assigned_section)
            except ObjectDoesNotExist:
                pass

        # Update the user for an existing Course/Section assignment with the assigned_user
        if updated_assignment is not None:
            updated_assignment.user_id = assigned_user
            updated_assignment.save()
        # Create a new assignment for the Course/Section with the assigned_user
        else:
            UserCourseAssignment.objects.create(user_id=assigned_user,
                                                course_id=assigned_course,
                                                section_id=assigned_section,
                                                section_type=assigned_section.section_type)

    return "successfully created the user assignment"


def remove_user_from(assigned_user, assigned_course):
    if not isinstance(assigned_course, Course):
        return "invalid course input"

    if not isinstance(assigned_user, User) or not User.objects.filter(user_id=assigned_user.user_id).exists():
        return "user does not exist"

    for assignment in UserCourseAssignment.objects.filter(course_id=assigned_course, user_id=assigned_user):
        assignment.delete()

    return "User successfully removed from this course."
