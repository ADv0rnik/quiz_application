from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from questions.models import Question, Answer
from quizzes.models import Quiz
from results.models import Results


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


def quiz_data_view(request, pk):
    data = Quiz.objects.get(pk=pk)
    questions = []
    for q in data.get_question():
        answers = []
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
    })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def save_quiz_data(request, pk):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        for key in data_.keys():
            question = Question.objects.get(text=key)
            questions.append(question)

        user = request.user
        quiz_ = Quiz.objects.get(pk=pk)
        score = 0
        c = 100 / quiz_.number_of_questions  # coefficient that define a value to recalculate the score
        results = []
        correct_answer = None

        # Checking for correct answers
        for q_ in questions:
            answer_selected = request.POST.get(q_.text)
            if answer_selected != "":
                question_answers = Answer.objects.filter(question=q_)
                for answer in question_answers:
                    if answer_selected == answer.text:
                        score += 1
                        correct_answer = answer.text
                    else:
                        correct_answer = answer.text
                results.append({str(q_): {'correct answer': correct_answer, 'answered': answer_selected}})
            else:
                results.append({str(q_): 'missed'})

        score_ = score * c
        Results.objects.create(quiz=quiz_, user=user, score=score_)
        if score_ >= quiz_.score:
            return JsonResponse({'passed': True, 'score': score_, "results": results})
        else:
            return JsonResponse({'passed': False, 'score': score_, "results": results})


def index(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
