from .models import Course, Section
from django.core.exceptions import ObjectDoesNotExist
'''
course_id is immutable
'''

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
    course.course_description=new_course_description if new_course_description != '' else course.course_description
    course.course_code=new_course_code if new_course_code != '' else course.course_code
    course.save()
    return True

def delete_course(course):
    if Section.objects.filter(course_id=course).exists():
        return False
    return course.delete()