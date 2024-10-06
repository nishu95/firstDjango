from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_login_view, name='teacher_login'),
    path('teacher/dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_login_view, name='student_dashboard'),
    path('student/dashboard', views.student_dashboard, name='student_dashboard'),
    path('admin/', views.admin_login_view, name='admin_login'),
    path('admin/custom-admin-user-form/', views.custom_admin_user_form, name='custom_admin_user_form'),
    # Add more student-related routes here
]
