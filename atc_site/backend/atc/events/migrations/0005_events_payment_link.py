# Generated by Django 4.1.2 on 2024-04-04 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_eventschedule_event_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='payment_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]