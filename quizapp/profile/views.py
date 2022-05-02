from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from .forms import CreateUserForm, StudentForm, UpdateStudentForm
from django.contrib import messages
from .decorators import *
from django.db.models import Max

from .models import Student


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
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
    group = student.user.groups.all()[0].name
    results = student.get_results().order_by('-date_created')[:5]
    max_score = results.aggregate(Max('score')).get('score__max')
    quiz_count = student.get_results().filter(passed=True).count()
    context = {
        'username': request.user,
        "student": student,
        "group": group,
        "results": results,
        "max_score": max_score,
        "count": quiz_count,
    }
    return render(request, 'user_page.html', context)


@allowed_user(allowed_roles=['student'])
def update_profile(request):
    student_ = Student.objects.get(user=request.user)
    form = StudentForm(instance=student_)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student_)
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
    gr = supervisor.user.groups.all()[0].name
    output = []
    for stdnt in students:
        max_score = stdnt.get_results().filter(student=stdnt.id).aggregate(Max('score')).get('score__max')
        quiz_count = stdnt.get_results().filter(passed=True).count()
        recent_quiz = stdnt.get_results().order_by('-date_created').first().quiz.name
        output.append({
            "id": stdnt.id,
            "name": stdnt.first_name,
            "surname": stdnt.last_name,
            "department": stdnt.department,
            "score": max_score,
            "passed": quiz_count,
            "recent_quiz": recent_quiz,
        })
    print(output)

    context = {"username": request.user,
               "supervisor": supervisor,
               "group": gr,
               "results": output}
    return render(request, 'supervisor.html', context)


@supervisor_only
def update_admin(request):
    supervisor_ = Student.objects.get(user=request.user)
    form = StudentForm(instance=supervisor_)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=supervisor_)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was updated for ' + str(request.user))

    context = {
        "username": request.user,
        "form": form
    }
    return render(request, 'supervisor_update_page.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def student(request, pk):
    stdnt_ = Student.objects.get(id=pk)
    results = stdnt_.get_results().order_by('-date_created')[:5]
    max_score = results.aggregate(Max('score')).get('score__max')
    quiz_count = stdnt_.get_results().filter(passed=True).count()
    gr_ = stdnt_.user.groups.all()[0].name
    context = {
        "student": stdnt_,
        "group": gr_,
        "results": results,
        "max_score": max_score,
        "count": quiz_count,
    }
    return render(request, 'student.html', context)


# Changing status of users here
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def update_student(request, pk):
    st = Student.objects.get(pk=pk)
    form = UpdateStudentForm(instance=st)
    if request.method == "POST":
        form = UpdateStudentForm(request.POST, instance=st)
        if form.is_valid():
            form.save()
            gr = request.POST.get('group')
            group = Group.objects.get(name=gr)
            st.user.groups.clear()
            group.user_set.add(st.user)
            messages.success(request, 'Account was updated for ' + str(st.user))
    context = {
        "student": st,
        "form": form,
    }
    return render(request, 'supervisor_to_student.html', context)
