from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import CreateUserForm, StudentForm
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_user
from django.db.models import Max

from .models import Student


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            Student.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                mail=email,
            )
            group_name = Group.objects.get(name='student')
            user.groups.add(group_name)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('home')
            else:
                login(request, user)
                return redirect('user', username=username)
        else:
            messages.info(request, 'Username or password do not match')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'home.html')


@allowed_user(allowed_roles=['student'])
def user_page(request, username):
    student = Student.objects.get(user=request.user)
    results = student.get_results().order_by('-date_created')[:5]
    max_score = results.aggregate(Max('score')).get('score__max')
    quiz_count = student.get_results().filter(passed=True).count()
    print(quiz_count)


    # for result in results:
    #     print(result.quiz, result.quiz.topic, result.score, result.date_created, result.passed)

    context = {
        'username': request.user,
        "student": student,
        "results": results,
        "max_score": max_score,
        "count": quiz_count,
    }

    return render(request, 'user_page.html', context)


@login_required
@allowed_user(allowed_roles=['student'])
def update_profile(request, username):
    student = Student.objects.get(user=request.user)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()

    context = {
        "username": request.user,
        "form": form
    }
    return render(request, 'user_update_page.html', context)




