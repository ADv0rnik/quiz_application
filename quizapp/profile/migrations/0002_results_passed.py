# Generated by Django 4.0.3 on 2022-04-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='passed',
            field=models.BooleanField(default=False, help_text='result of taken quiz'),
        ),
    ]