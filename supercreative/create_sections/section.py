from supercreative.models import Course, Section, User, UserCourseAssignment
from django.core.exceptions import ObjectDoesNotExist


def create_section(section_id, course, section_type, user):
    # Preconditions

    if not isinstance(user, User):
        return "invalid input for user"

    # Check if the SectionID is a valid int
    if not isinstance(section_id, int) or section_id < 1:
        return "sectionID must be an integer"

    # Check if the course param is of the correct type
    if not isinstance(course, Course):
        return "invalid input for course"

    # Check if the course is in the courses table
    try:
        Course.objects.get(course_id=course.course_id)
    except ObjectDoesNotExist:
        return "course does not exist"

    # Check if the SectionID already exists in the Sections table
    if Section.objects.filter(section_id=section_id).exists():
        return "section already exists"

    # Check if Section Type is valid: "Lecture", "Lab", or "Discussion"
    valid_section_types = ["LECTURE", "LAB", "DISCUSSION"]

    if section_type is None or section_type.upper() not in valid_section_types:
        return "section type is not valid"

    # Post conditions
    # Create an entry in the Sections table with the input information
    new_section = Section(
        section_id=section_id,
        course_id=course,
        section_type=section_type.lower()
    )
    new_section.save()

    new_user_course_assignment = UserCourseAssignment(
        user_id=user,
        section_id=new_section,
        course_id=course,
        section_type=section_type
    )

    new_user_course_assignment.save()

    # Return true if input was valid
    return "section was successfully created"
