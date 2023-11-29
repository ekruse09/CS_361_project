from supercreative.models import Course, Section
from django.core.exceptions import ObjectDoesNotExist


def create_course(id, name, description, code):
    # check for valid id
    if not (isinstance(id, int) and id > 0):
        return False

    # check for valid name
    if not (isinstance(name, str)):
        return False

    # check for valid description
    if not isinstance(description, str):
        return False

    # check for valid course code (just checking for a unique string as of now)
    if not (isinstance(code, str)):
        return False

    # check database for duplicate ids, names, or course codes
    if Course.objects.filter(course_id=id).exists() or Course.objects.filter(
            course_name=name).exists() or Course.objects.filter(course_code=code).exists():
        return False

    # create the course
    new_course = Course(
        course_id=id,
        course_name=name,
        course_description=description,
        course_code=code
    )
    new_course.save()

    return True


def edit_course(current_course_id, new_course_name='', new_course_description="", new_course_code=""):
    course = Course.objects.get(course_id=current_course_id)
    existing_course = None
    try:
        existing_course = Course.objects.get(course_name=new_course_name)
    except ObjectDoesNotExist:
        pass

    try:
        existing_course = Course.objects.get(course_code=new_course_code)
    except ObjectDoesNotExist:
        pass

    if existing_course is not None:
        return False

    course.course_name = new_course_name if new_course_name != '' else course.course_name
    course.course_description = new_course_description if new_course_description != '' else course.course_description
    course.course_code = new_course_code if new_course_code != '' else course.course_code
    course.save()
    return True


def delete_course(course):
    if Section.objects.filter(course_id=course).exists():
        return False
    Course.objects.get(course_id=course.course_id).delete()
    return True
