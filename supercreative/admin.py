from django.contrib import admin
from .models import User, Course, Section, UserCourseAssignment
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(UserCourseAssignment)