# Generated by Django 4.0.3 on 2022-03-21 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type_of_answer',
            field=models.CharField(default='', max_length=20),
        ),
    ]
