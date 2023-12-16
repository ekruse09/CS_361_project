from supercreative.models import Course, Section, UserCourseAssignment, SectionType
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
        if UserCourseAssignment.objects.filter(user_id=assigned_user,
                                               course_id=assigned_course,
                                               section_id=assigned_section).exists():
            return "assignment already exists"
        UserCourseAssignment.objects.create(user_id=assigned_user,
                                            course_id=assigned_course,
                                            section_id=assigned_section,
                                            section_type=assigned_section.section_type)

    return "successfully created the user assignment"
