# Generated by Django 2.0.4 on 2018-05-29 16:09

import device.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_auto_20180513_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='uploader',
        ),
        migrations.AlterField(
            model_name='version',
            name='file',
            field=models.FileField(null=True, upload_to=device.models.uploaded_file_path),
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
