# Generated by Django 3.0.8 on 2020-10-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201013_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Resume',
            field=models.FileField(default='Sample.pdf', upload_to='Resume'),
        ),
    ]
