from django.urls import path
from .views import (
    QuizListView,
    quiz,
    quiz_data,
)

urlpatterns = [
    path('', quiz, name='quiz'),
    path('<int:pk>/', quiz_data, name='quiz-data'),
]
