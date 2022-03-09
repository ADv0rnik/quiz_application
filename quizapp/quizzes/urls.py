from django.urls import path
from .views import (
    QuizListView,
    quiz
)

urlpatterns = [
    path('', quiz, name='quiz')
]
