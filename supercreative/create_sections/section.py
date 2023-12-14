from supercreative.models import Course, Section
from django.core.exceptions import ObjectDoesNotExist


def create_section(section_id, course, section_type):
    # Preconditions

    # Check if the SectionID is a valid int
    if not isinstance(section_id, int) or section_id < 1:
        return False

    # Check if the course param is of the correct type
    if not isinstance(course, Course):
        return False

    # Check if the course is in the courses table
    try:
        Course.objects.get(course_id=course.course_id)
    except ObjectDoesNotExist:
        return False

    # Check if the SectionID already exists in the Sections table
    if Section.objects.filter(section_id=section_id).exists():
        return False

    # Check if Section Type is valid: "Lecture", "Lab", or "Discussion"
    valid_section_types = ["LECTURE", "LAB", "DISCUSSION"]

    if section_type is None or section_type.upper() not in valid_section_types:
        return False

    # Post conditions
    # Create an entry in the Sections table with the input information
    new_section = Section(
        section_id=section_id,
        course_id=course,
        section_type=section_type.lower()
    )
    new_section.save()

    # Return true if input was valid
    return True