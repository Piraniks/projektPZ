# Generated by Django 2.0.4 on 2018-06-02 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_auto_20180602_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='file_checksum',
            field=models.BinaryField(blank=True),
        ),
    ]