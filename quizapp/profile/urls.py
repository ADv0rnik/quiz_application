from django.urls import path
from .views import (
    register_user,
    login_user,
    logout_user,
    user_page,
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('<username>/', user_page, name='user'),
]
