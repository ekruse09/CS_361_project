from django.db import models


class UserRole(models.Model):
    role_id = models.BigAutoField(unique=True, primary_key=True)
    role_name = models.CharField(max_length=50)


class User(models.Model):
    user_id = models.BigAutoField(unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role_id = models.ForeignKey(UserRole, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    skills = models.TextField(max_length=1000, default='', null=True)


class Course(models.Model):
    course_id = models.BigAutoField(unique=True, primary_key=True)
    course_name = models.CharField(max_length=255)
    course_description = models.CharField(max_length=1000)
    course_code = models.CharField(max_length=20)


class SectionType(models.Model):
    section_type_id = models.BigAutoField(unique=True, primary_key=True)
    section_type_name = models.CharField(max_length=50)


class Section(models.Model):
    section_id = models.BigAutoField(unique=True, primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.DO_NOTHING)


class UserCourseAssignment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE, null=True)

    # # Enforces that a user can only be assigned to a course once
    # class Meta:
    #     unique_together = ('user_id', 'course_id')
    #     app_label = 'supercreative'
