# Generated by Django 4.0.3 on 2022-05-02 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_results_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='pic',
        ),
    ]
