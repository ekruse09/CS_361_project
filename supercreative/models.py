from django.db import models

class User(models.Model):
    user_id = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

class Course(models.Model):
    course_id = models.IntegerField(unique=True)
    course_name = models.CharField(max_length=255)
    course_description = models.CharField(max_length=1000)
    course_code = models.CharField(max_length=20)


class Section(models.Model):
    section_id = models.IntegerField(unique=True, primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=50)

class UserCourseAssignment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=50)




    # # Enforces that a user can only be assigned to a course once
    # class Meta:
    #     unique_together = ('user_id', 'course_id')
    #     app_label = 'supercreative'

