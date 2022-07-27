# Generated by Django 3.1 on 2021-04-21 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='visible',
            field=models.CharField(choices=[('P', 'Public'), ('F', 'Following')], default=1, max_length=1, verbose_name='Görünüm'),
        ),
    ]
