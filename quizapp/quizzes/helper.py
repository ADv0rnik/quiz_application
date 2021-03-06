import re

from quizzes.models import Quiz


def get_available_quizzes(stack, department="all") -> list:
    """
    The function collects all quizzes assigned to certain quiz taker in accordance to his/her technology stack and department

    :param stack: set of technologies that helps to filter relevant quizzes from database
    :param department: string type, name of the department.
                       Helps to filter quizzes that have been assigned to this department
    :return: list of quizzes
    """
    quizzes = []
    for item in stack:
        list_of_quizzes = Quiz.objects.filter(stack=item.name)
        assigned_quizzes = Quiz.objects.filter(assigned_to=department).filter(stack="common")
        for quiz in list_of_quizzes:
            quizzes.append(quiz)
        for assigned in assigned_quizzes:
            quizzes.append(assigned)
    return quizzes


def get_quizzes_storage(results, quizzes):
    """
    The function creates a storage of data related to quizzes taken by user

    :param results: set of results obtained by user
    :param quizzes: list of quizzes derived from "get_available_quizzes" (see helper.py) function
    :return: nested dictionary of relevant information, including "name", "topic", "difficulty", "status" etc.
    """
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
    """
    Helper function that clean specified dictionary from undesired symbols

    :param var: dictionary of keys and values, where key is "question" and value is the list of answers
    :return: clean dictionary where keys and values are presented in lowercase
    """
    new_dict = {}
    pattern = '[A-z??-??0-9\,\(\)\s]*\?'
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
