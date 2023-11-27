from supercreative.models import (Course, Section)


def create_course(id, name, description, code, role):

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

    # checking for appropriate privileges
    if role != "administrator":
        return False

    # check database for duplicate ids, names, or course codes
    if Course.objects.filter(course_id=id).exists() or Course.objects.filter(course_name=name).exists() or Course.objects.filter(course_code=code).exists():
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
