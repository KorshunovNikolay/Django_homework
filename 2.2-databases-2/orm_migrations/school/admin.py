from django.contrib import admin

from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'display_teachers']
    list_filter = ['group', 'teachers']
    filter_horizontal = ['teachers']

    def display_teachers(self, student):
        return ', '.join([teacher.name for teacher in student.teachers.all()])
    display_teachers.short_description = 'Преподаватели'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'display_students']
    list_filter = ['subject', 'students']


    def display_students(self, teacher):
        return ', '.join([student.name for student in teacher.students.all()])
    display_students.short_description = 'Ученики'
