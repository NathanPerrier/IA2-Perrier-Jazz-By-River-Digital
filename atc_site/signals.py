from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

CUSTOM_GROUPS = ["Admin", "Student", "Teacher", "Parent", "User"]

@receiver(post_migrate)
def create_custom_groups(sender, **kwargs):
    for group_name in CUSTOM_GROUPS:
        Group.objects.get_or_create(name=group_name)

    print("Custom groups ensured.")