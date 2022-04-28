from django.http import HttpResponse
from django.shortcuts import redirect


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
            print('you are supervisor')
            return view_function(request, *args, **kwargs)
        else:
            print('you are not supervisor')
            return redirect('user', username=request.user)
    return wrapper
