from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Student
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        group_name = Group.objects.get(name='student')
        instance.groups.add(group_name)
        Student.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            mail=instance.email,
        )
        print('Profile created!')
