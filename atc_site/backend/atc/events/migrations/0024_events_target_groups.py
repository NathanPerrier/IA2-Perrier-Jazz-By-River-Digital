# Generated by Django 4.1.2 on 2024-04-12 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_alter_events_description_alter_events_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='target_groups',
            field=models.ManyToManyField(blank=True, to='auth.group'),
        ),
    ]