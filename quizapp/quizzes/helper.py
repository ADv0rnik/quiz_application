import re

from quizzes.models import Quiz


def get_available_quizzes(stack):
    quizzes = []
    for item in stack:
        list_of_quizzes = Quiz.objects.filter(stack=item.name)
        for quiz in list_of_quizzes:
            quizzes.append(quiz)
    return quizzes


def get_quizzes_storage(results, quizzes):
    quizzes_storage = {}
    for quiz in quizzes:
        for result in results:
            if quiz.id == result.quiz_id:
                res = {'name': quiz.name, 'topic': quiz.topic, 'number_of_questions': quiz.number_of_questions,
                       'time': quiz.time, 'score': quiz.score, 'difficulty': quiz.difficulty, 'status': 'Passed'}
                quizzes_storage[quiz.id] = res
            else:
                if quiz.id not in quizzes_storage:
                    res_ = {'name': quiz.name, 'topic': quiz.topic, 'number_of_questions': quiz.number_of_questions,
                            'time': quiz.time, 'score': quiz.score, 'difficulty': quiz.difficulty,
                            'status': 'Failed'}
                    quizzes_storage[quiz.id] = res_
                else:
                    continue
    return quizzes_storage


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
