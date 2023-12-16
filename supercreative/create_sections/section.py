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


def delete_section(delsection):
    if not delsection:
        return "No Section detected"
    try:
        section = Section.objects.get(section_id=delsection)
    except ObjectDoesNotExist:
        return "Section does not exist"
    UserCourseAssignment.objects.filter(section_id=section).delete()
    section.delete()
    return "Section deletion was successful"
