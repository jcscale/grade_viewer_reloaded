from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),

    ##### ADMIN #####
    path('adminpage/teachers', views.TeacherListView.as_view(), name='teacher-list'),
    path('adminpage/students', views.StudentListView.as_view(),
         name='admin-student-list'),
    path('adminpage/students/<int:pk>',
         views.StudentInformationView.as_view(), name='student-info'),
    path('adminpage/student-subjects/<int:pk>', views.StudentSubjectListView.as_view(),
         name='student-subjects'),
    path('adminpage/student-subjects/form/<int:pk>',
         views.StudentSubjectForm.as_view(), name='student-subjects-form'),


    ##### TEACHER #####
    # path('teacher/', views.teacher, name='teacher'),
    path('teacher', views.HomeStudentList.as_view(), name='teacher'),
    path('teacher/subjects/', views.TeacherSubjectListView.as_view(),
         name='teacher-subjects'),
    path('teacher/subjects/student-list/<int:subject_name_id>/<str:year_taken>/',
         views.StudentList.as_view(), name='student-list'),
    path('<pk>/update', views.GradeUpdateView.as_view(), name='grade-update'),
    path('password/', views.PasswordChangeView.as_view(
        template_name='register/change_password.html'), name='password-change'),
    path('password_success/', views.password_success, name='password_success'),


    ##### STUDENT #####
    path('student/', views.student, name='student'),
    path('<int:pk>', views.StudentSubjects.as_view(), name='student-grade'),
]
