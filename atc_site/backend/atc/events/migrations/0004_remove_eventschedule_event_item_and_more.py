# Generated by Django 4.1.2 on 2024-04-02 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_voucher_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventschedule',
            name='event_item',
        ),
        migrations.AddField(
            model_name='eventschedule',
            name='event_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.eventscheduleitem'),
            preserve_default=False,
        ),
    ]
