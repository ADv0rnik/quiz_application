from django.urls import path
from .views import (
    register_user,
    login_user,
    logout_user,
    user_page,
    update_profile,
    admin,
    update_admin,
    student,
    update_student,
    manage_quizzes,
    save_manage_quizzes,
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('user_page/', user_page, name='user'),
    path('user_page/update', update_profile, name='user_update'),

    path('supervisor/', admin, name='supervisor'),
    path('supervisor/update', update_admin, name='supervisor_update'),
    path('supervisor/manage_quizzes', manage_quizzes, name='manage_quizzes'),
    path('supervisor/manage_quizzes/save', save_manage_quizzes, name='save_manage_quizzes'),

    path('student/<str:pk>/', student, name='student'),
    path('student/<str:pk>/update/', update_student, name='student_update'),
]
