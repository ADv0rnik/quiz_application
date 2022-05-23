import re

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from profile.models import Results, Student
from questions.models import Question, Answer
from quizzes.models import Quiz


@login_required(login_url='login')
def quiz(request):
    student_stack = Student.objects.get(user=request.user).get_stack()
    quizzes = []
    for item in student_stack:
        list_of_quizzes = Quiz.objects.filter(stack=item.name)
        for quiz in list_of_quizzes:
            quizzes.append(quiz)
    context = {
        "quizzes": quizzes,
        "user": request.user,
    }
    return render(request, 'quizzes.html', context)


@login_required
def quiz_data(request, pk):
    q = Quiz.objects.get(pk=pk)
    return render(request, 'quiz.html', {"quiz": q})


def quiz_data_view(request, pk):
    data = Quiz.objects.get(pk=pk)
    time = data.time
    print(time)
    questions = []
    type_of_answers = []
    for q in data.get_question():
        type_of_answers.append(q.type_of_answer)
        answers = []
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'type': type_of_answers,
        'time': time,
    })


def clear_data(var):
    new_dict = {}
    pattern = '[A-zА-я0-9\,\(\)\s]*\?'
    for key, val in var.copy().items():
        if len(val) > 1:
            new_val = val[1:]
        else:
            new_val = val
        new_key = re.findall(pattern, key)
        if new_key[0] not in new_dict:
            new_dict[new_key[0]] = sorted(new_val)
    return to_lower_case(new_dict)


def to_lower_case(dictionary):
    for key, value in dictionary.items():
        for v in range(len(value)):
            value[v] = value[v].lower()
    return dictionary


# a function to check correct answer for questions with multiple choice.
# The "local_score" variable is a counter for correct answers. Positive values correspond to correct answers
def check_answers(selected, actual):
    local_score = 0
    correct_answers = []
    for selected_answer in selected:
        answers = []
        for answer in actual:
            if answer.text.lower() == selected_answer and answer.correct:
                answers.append(1)
                correct_answers.append(answer.text.lower())
            else:
                answers.append(0)
                if answer.correct:
                    correct_answers.append(answer.text.lower())
        if 1 in answers:
            local_score += 1
        else:
            local_score -= 1
    return {
        'score': local_score,
        'correct': sorted(list(set(correct_answers)))
    }


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def save_quiz_data(request, pk):
    if is_ajax(request=request):
        questions = []
        data = dict(request.POST.lists())
        data.pop('csrfmiddlewaretoken')
        data_ = clear_data(data)
        print(data_)
        for key in data_.keys():
            try:
                question = Question.objects.select_related('quiz').get(text=key)
            except questions.models.Question.DoesNotExist as error:
                print(error)
            else:
                questions.append(question)
        user = request.user
        student = Student.objects.filter(user=user)[0]
        quiz_ = Quiz.objects.get(pk=pk)
        score = 0
        c = 100 / quiz_.number_of_answers  # coefficient that define a value to recalculate the score
        results = []

        for q_ in questions:
            answers_selected = data_.get(q_.text)
            question_answers = Answer.objects.filter(question=q_)
            if answers_selected[0] != '':
                answers_checked = check_answers(answers_selected, question_answers)
                single_score = answers_checked['score']
                if single_score > 0:
                    score += single_score
                else:
                    score += 0
                results.append(
                    {str(q_): {'correct answer': answers_checked['correct'], 'your answer': answers_selected}})
            else:
                results.append({str(q_): 'missed'})
        score_ = score * c
        print(results)

        if score_ >= quiz_.score:
            Results.objects.create(quiz=quiz_, score=round(score_, 2), student=student, passed=True)
            return JsonResponse({'passed': True, 'score': round(score_, 2), "results": results})
        else:
            Results.objects.create(quiz=quiz_, score=round(score_, 2), student=student, passed=False)
            return JsonResponse({'passed': False, 'score': round(score_, 2), "results": results})


def index(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
