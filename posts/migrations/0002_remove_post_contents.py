# Generated by Django 3.1 on 2021-04-19 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='contents',
        ),
    ]
