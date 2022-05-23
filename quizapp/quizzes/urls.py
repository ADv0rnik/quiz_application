from django.urls import path
from .views import (
    quiz,
    quiz_data,
    quiz_data_view,
    save_quiz_data,
)

urlpatterns = [
    path('', quiz, name='quiz'),
    path('<int:key>/', quiz_data, name='quiz-data'),
    path('<int:pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('<int:pk>/save/', save_quiz_data, name='save-data'),
]
