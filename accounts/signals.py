from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import AppUser


@receiver(post_save, sender=AppUser)
def assign_user_group(sender, instance, created, **kwargs):

    if instance.role == "manager":
        group_name = "Managers"
    else:
        group_name = "Users"

    group, _ = Group.objects.get_or_create(name=group_name)

    # махаме всички групи
    instance.groups.clear()

    # добавяме правилната
    instance.groups.add(group)