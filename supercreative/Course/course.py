import models

def create_course(course_id, course_name, course_description, course_code):
    course = models.Course.objects.create(course_id=course_id, course_name=course_name, course_description=course_description, course_code=course_code)
    return course

def check_existence(course_id):
    exists = models.Course.objects.filter(course_id=course_id).exists()
    return exists

def nonexistense_error():
    redirect('/course/nonexistantcourse')

def edit_course(course_id, course_name, course_description, course_code):
    course = models.Course.objects.get(course_id=course_id)
    course.course_name = course_name
    course.course_description = course_description
    course.course_code = course_code
    course.save()
    return course

def delete_course(course_id):
    course = models.Course.objects.get(course_id=course_id)
    course.delete()