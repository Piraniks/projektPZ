# Generated by Django 2.0.4 on 2018-05-13 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0002_device_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='latest_version',
            new_name='version',
        ),
    ]
