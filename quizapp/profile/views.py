from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, StudentForm
from django.contrib import messages
from .decorators import *
from django.db.models import Max

from .models import Student


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, )
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password do not match')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return render(request, 'home.html')


@login_required
@allowed_user(allowed_roles=['student'])
def user_page(request):
    student = Student.objects.get(user=request.user)
    results = student.get_results().order_by('-date_created')[:5]
    max_score = results.aggregate(Max('score')).get('score__max')
    quiz_count = student.get_results().filter(passed=True).count()
    context = {
        'username': request.user,
        "student": student,
        "results": results,
        "max_score": max_score,
        "count": quiz_count,
    }
    return render(request, 'user_page.html', context)


@allowed_user(allowed_roles=['student'])
def update_profile(request):
    student = Student.objects.get(user=request.user)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was updated for ' + str(request.user))

    context = {
        "username": request.user,
        "form": form
    }
    return render(request, 'user_update_page.html', context)


@login_required(login_url='login')
@supervisor_only
def admin(request):
    students = Student.objects.select_related('user').all().exclude(user=1)
    supervisor = students.filter(user=request.user)[0]
    output = []
    for student in students:
        max_score = student.get_results().filter(student=student.id).aggregate(Max('score')).get('score__max')
        quiz_count = student.get_results().filter(passed=True).count()
        recent_quiz = student.get_results().order_by('-date_created').first().quiz.name
        output.append({
            "id": student.id,
            "name": student.first_name,
            "surname": student.last_name,
            "department": student.department,
            "score": max_score,
            "passed": quiz_count,
            "recent_quiz": recent_quiz,
        })
    print(output)

    context = {"username": request.user,
               "supervisor": supervisor,
               "results": output}
    return render(request, 'supervisor.html', context)
