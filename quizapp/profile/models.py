from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from quizzes.models import Quiz


STACK_CHOICE = [
    ('python', 'python'),
    ('linux', 'linux'),
    ('java', 'java'),
]


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.CharField(max_length=100)
    department = models.CharField(max_length=200, default='')
    occupation = models.CharField(max_length=200, default='developer')
    pic = models.ImageField(default="default.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"ID: {self.pk} Name: {self.user}"

    def get_results(self):
        return self.results_set.all()

    def get_stack(self):
        return self.techstack_set.all()

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.user})

    class Meta:
        verbose_name_plural = 'Students'


class Results(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False, help_text='result of taken quiz')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Results_ID: {self.pk}"

    def get_quiz(self):
        return self.quiz_set.all()

    class Meta:
        verbose_name_plural = 'Results'


class TechStack(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='technology name',
        choices=STACK_CHOICE,
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student}: {self.name}"

    class Meta:
        verbose_name_plural = "Technologies"
