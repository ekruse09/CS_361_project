from supercreative.models import (Course, Section)


def create_course(id, name, description, code, role):

    # check to see if the id, name, description, code, and role are valid
    if not (isinstance(id, int) and id > 0):
        return False

    if not (isinstance(name, str)):
        return False

    if not isinstance(description, str):
        return False

    if not (isinstance(code, str)):
        return False

    if role != "administrator":
        return False

    # check database for duplicate courses
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
