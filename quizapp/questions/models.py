from django.db import models
from quizapp.quizzes.models import Quiz


class Question(models.Model):
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_answer(self):
        return self.answer_set.all()


# set answers class
