from supercreative.models import Course, Section, SectionType, UserCourseAssignment
from django.core.exceptions import ObjectDoesNotExist


def create_section(course, section_type):
    # Preconditions

    # Check if the course param is of the correct type
    if not isinstance(course, Course):
        return "invalid input for course"

    # Check if the course is in the courses table
    try:
        Course.objects.get(course_id=course.course_id)
    except ObjectDoesNotExist:
        return "course does not exist"

    if not SectionType.objects.filter(section_type_name=section_type).exists():
        return "section type is not valid"

    # Post conditions
    # Create an entry in the Sections table with the input information
    new_section = Section(
        course_id=course,
        section_type=SectionType.objects.get(section_type_name=section_type)
    )
    new_section.save()

    # Return true if input was valid
    return "section was successfully created"


def delete_section(course_id, section_id):
    # if not section_id:
    #     return "No Section detected"
    try:
        section = Section.objects.get(course_id=course_id,section_id=section_id)
    except ObjectDoesNotExist:
        return "Section does not exist"
    UserCourseAssignment.objects.filter(course_id=Course.objects.get(course_id=course_id),section_id=section).delete()
    Section.objects.filter(course_id=Course.objects.get(course_id=course_id),section_id=section_id).delete()
    try:
        Section.objects.get(course_id=Course.objects.get(course_id=course_id), section_id=section_id)
    except ObjectDoesNotExist:
        return "Section deletion was successful"
    return "Failed to delete section"

def get_sections(course):
    user_assignments = UserCourseAssignment.objects.filter(course_id=course)
    course_sections = Section.objects.filter(course_id=course)
    uca_sections = {}
    for section in course_sections:
        current_uca = None
        try:
            current_uca = user_assignments.get(course_id=course, section_id=section)
        except ObjectDoesNotExist:
            current_uca = ""
        uca_sections[section] = current_uca

    return uca_sections