from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from quizzes.models import Quiz


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.CharField(max_length=100, help_text='email address')
    department = models.CharField(max_length=200, default='')
    occupation = models.CharField(max_length=200, default='developer')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"ID: {self.pk} Name: {self.user}"

    def get_results(self):
        return self.results_set.all()

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

    class Meta:
        verbose_name_plural = 'Results'
