from django.shortcuts import render
from django.views.generic import ListView
from quizzes.models import Quiz


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz.html'


def quiz_view(request, pk):
    pass


def quiz(request):
    return render(request, 'quiz.html')


def index(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


