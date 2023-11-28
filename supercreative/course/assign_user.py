from supercreative.models import User, Course, Section, UserCourseAssignment
from django.core.exceptions import ObjectDoesNotExist

# section assignment not implemented until sprint 2
def assign_user_to(assigned_user, assigned_course, assigned_section=None):
    try:
        if assigned_course is None or UserCourseAssignment.objects.filter(user_id=assigned_user,
                                                                          course_id=assigned_course,
                                                                          section_id=assigned_section).exists():
            return False
    except ObjectDoesNotExist:
        pass

    UserCourseAssignment.objects.create(user_id=assigned_user, course_id=assigned_course,section_id=assigned_section,
                                        section_type='' if assigned_section is None else Section.objects.get
                                        (section_id=assigned_section.section_id).section_type)
    return True
