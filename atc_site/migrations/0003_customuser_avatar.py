# Generated by Django 4.1.2 on 2024-02-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atc_site', '0002_customuser_is_active_customuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/avatar/'),
        ),
    ]