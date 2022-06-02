# Generated by Django 4.0.3 on 2022-06-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0012_alter_techstack_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techstack',
            name='name',
            field=models.CharField(choices=[('python', 'python'), ('linux', 'linux'), ('java', 'java')], help_text='technology name', max_length=100),
        ),
    ]
