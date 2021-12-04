from django.contrib import admin
from .models import User, Subject, Student, SchoolSubject, Teacher, Course
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Role',
            {
                'fields': (
                    'is_admin',
                    'is_teacher',
                    'is_student',
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Teacher)


class SubjectInLine(admin.TabularInline):
    model = Subject
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'id_number']
    search_fields = ['name__username', 'id_number']
    inlines = [SubjectInLine]


class SchoolSubjectAdmin(admin.ModelAdmin):
    search_fields = ['subject_name']


# class TeacherSubjectsAdmin(admin.ModelAdmin):
#     list_display = ['subject_name']
#     search_fields = ['teacher_name', 'subject_name']
#     extra = 2


# admin.site.register(TeacherSubject, TeacherSubjectsAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(SchoolSubject)
admin.site.register(Course)
