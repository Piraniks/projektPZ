# Generated by Django 2.0.4 on 2018-06-06 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0011_auto_20180605_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicegroup',
            old_name='version',
            new_name='_version',
        ),
    ]