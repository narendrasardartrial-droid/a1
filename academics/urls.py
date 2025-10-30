from django.urls import path
from . import views


urlpatterns = [
    path('teacher/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    path('create-teacher-step1/', views.create_teacher_step1, name='create_teacher_step1'),
    path('create-teacher-step2/', views.create_teacher_step2, name='create_teacher_step2'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path("student/<int:student_id>/", views.student_profile, name="student_profile"),
    path("student/step1/", views.create_student_step1, name="create_student_step1"),
    path("student/step2/", views.create_student_step2, name="create_student_step2"),
    path('computer-engineering/', views.computer_engineering, name='computer_engineering'),
    path('it-engineering/', views.it_engineering, name='it_engineering'),
    path('electrical-engineering/', views.electrical_engineering, name='electrical_engineering'),
    path('ai-ds-engineering/', views.ai_ds_engineering, name='ai_ds_engineering'),
    path('civil-engineering/', views.civil_engineering, name='civil_engineering'),
    path('mechanical-engineering/', views.mechanical_engineering, name='mechanical_engineering'),
    path('electronics-telecommunication-engineering/', views.electronics_telecom_engineering, name='electronics_telecom_engineering'),
]
