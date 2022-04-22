from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.user.username
            return redirect('user', username=username)
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
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper
    return decorator
