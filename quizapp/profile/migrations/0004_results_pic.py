# Generated by Django 4.0.3 on 2022-05-02 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_student_department_student_occupation'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
