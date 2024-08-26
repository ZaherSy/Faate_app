from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(CourseStudent)
admin.site.register(CourseTeacher)
admin.site.register(Session)
admin.site.register(StudentSession)
