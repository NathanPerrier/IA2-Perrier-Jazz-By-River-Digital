from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

CUSTOM_GROUPS = ["Admin", "Student", "Teacher", "Parent", "User", "Vendor", "Staff", "Organizer", "Volunteer", "Guest", 
                 "Year 4", "Year 5", "Year 6", "Year 7", "Year 8", "Year 9", "Year 10", "Year 11", "Year 12"]

@receiver(post_migrate)
def create_custom_groups(sender, **kwargs):
    for group_name in CUSTOM_GROUPS:
        Group.objects.get_or_create(name=group_name)

    print("Custom groups ensured.")