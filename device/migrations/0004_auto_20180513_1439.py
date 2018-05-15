# Generated by Django 2.0.4 on 2018-05-13 12:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20180513_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='last_edited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='device',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
