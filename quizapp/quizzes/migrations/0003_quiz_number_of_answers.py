# Generated by Django 4.0.3 on 2022-03-29 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_alter_quiz_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='number_of_answers',
            field=models.IntegerField(default=0),
        ),
    ]