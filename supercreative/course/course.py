from supercreative.models import Course, Section
from django.core.exceptions import ObjectDoesNotExist


def create_course(course_id, name, description, code):
    # check for valid id
    if not (isinstance(course_id, int) and course_id > 0):
        return "Course ID must be a positive integer."

    # check for valid name
    if not (isinstance(name, str)):
        return "Course name must be a string."

    # check for valid description
    if not isinstance(description, str):
        return "Course description must be a string."

    # check for valid course code (just checking for a unique string as of now)
    if not (isinstance(code, str)):
        return "Course code must be a string."

    # check database for duplicate ids, names, or course codes
    if Course.objects.filter(course_id=course_id).exists() or Course.objects.filter(
            course_name=name).exists() or Course.objects.filter(course_code=code).exists():
        return "Course ID, name, or code already exists."

    # create the course
    new_course=Course.objects.create(
        course_id=course_id,
        course_name=name,
        course_description=description,
        course_code=code
    )
    new_course.save()

    return "Course created successfully."


def edit_course(current_course_id, new_course_name='', new_course_description="", new_course_code=""):

    existing_course = False

    try:
        existing_course = (Course.objects.get(course_id=current_course_id) !=
                           Course.objects.get(course_code=new_course_code))
    except ObjectDoesNotExist:
        pass

    try:
        existing_course = (Course.objects.get(course_id=current_course_id) !=
                           Course.objects.get(course_name=new_course_name))
    except ObjectDoesNotExist:
        pass

    if existing_course is True:
        return "Course code, or name already exists."

    if Course.objects.filter(course_id=current_course_id).exists():
        course = Course.objects.get(course_id=current_course_id)
    else:
        return "Course does not exist."

    course.course_name = new_course_name if new_course_name != '' else course.course_name
    course.course_description = new_course_description if new_course_description != '' else course.course_description
    course.course_code = new_course_code if new_course_code != '' else course.course_code
    course.save()

    return "Course edited successfully."


def delete_course(course):
    if Course.objects.filter(course_id=course.course_id).exists():
        Course.objects.get(course_id=course.course_id).delete()
        return "Course deleted successfully."
    return "Course does not exist."

def course_id_to_int(course_id):
    try:
        return int(course_id)
    except:
        return None
