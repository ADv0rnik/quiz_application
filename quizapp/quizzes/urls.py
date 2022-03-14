from django.urls import path
from .views import (
    QuizListView,
    quiz,
    quiz_data,
    quiz_data_view,
)

urlpatterns = [
    path('', quiz, name='quiz'),
    path('<int:pk>/', quiz_data, name='quiz-data'),
    path('<int:pk>/data/', quiz_data_view, name='quiz-data-view'),
]
