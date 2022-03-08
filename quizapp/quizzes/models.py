from django.db import models

# Create your models here.
DIFF_CHOICE = [
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
]


class Quiz(models.Model):
    name = models.CharField(max_length=150)
    topic = models.CharField(max_length=150)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text='duration of the quiz')
    score = models.IntegerField(help_text='required score to pass the quiz')
    difficulty = models.CharField(max_length=50, choices=DIFF_CHOICE)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_question(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quizes'
