from django.shortcuts import render
from django.views.generic import ListView
from quizzes.models import Quiz


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizzes.html'


def quiz_view(request, pk):
    pass


def quiz(request):
    quiz1 = Quiz.objects.get(pk=1)
    quiz2 = Quiz.objects.get(pk=2)
    context = {
        "quiz_1": quiz1,
        "quiz_2": quiz2
    }
    return render(request, 'quizzes.html', context)


def quiz_data(request, pk):
    q = Quiz.objects.get(pk=pk)
    return render(request, 'quiz.html', {"quiz": q})


def index(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


