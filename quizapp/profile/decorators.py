from django.http import HttpResponse
from django.shortcuts import redirect

# tools for query debug
from django.db import connection, reset_queries
import time
import functools


def unauthenticated_user(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                print(f'Allowed. You entered as {group}')
                return view_func(request, *args, **kwargs)
            else:
                print(f'Not allowed. You are {group}')
                return HttpResponse('You are not authorized to view this page')
        return wrapper
    return decorator


def supervisor_only(view_function):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            print('you are a supervisor')
            return view_function(request, *args, **kwargs)
        else:
            print('you are not a supervisor')
            return redirect('user')
    return wrapper


def query_debugger(func):
    """Decorator for testing query execution time. Returns time in sec"""

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result
    return inner_func
