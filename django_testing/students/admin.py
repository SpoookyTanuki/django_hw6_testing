from django.contrib import admin
from students.models import Course, Student


class InLine(admin.TabularInline):
    model = Course.students.through


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [InLine, ]
