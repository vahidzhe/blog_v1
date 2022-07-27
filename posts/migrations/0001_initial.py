# Generated by Django 3.1 on 2021-04-19 08:07

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Kateqoriya')),
            ],
            options={
                'verbose_name': 'Kateqoriya',
                'verbose_name_plural': 'Kaetqoriyalar',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Başlığ')),
                ('slug', models.SlugField(default='', editable=False, max_length=122, unique=True, verbose_name='Slug yeri')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Məzmun')),
                ('contents', ckeditor.fields.RichTextField(verbose_name='Məzmun')),
                ('image', models.ImageField(blank=True, default='default.png', upload_to=posts.models.upload_to, verbose_name='Şəkil')),
                ('draft', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(related_name='post', to='posts.Category', verbose_name='Kateqoriya')),
                ('user', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Məqalə',
                'verbose_name_plural': 'Məqalələr',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, verbose_name='Məzmun')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='posts.post', verbose_name='Məqalə')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Şərh',
                'verbose_name_plural': 'Şərhlər',
            },
        ),
        migrations.CreateModel(
            name='ChildComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='Məzmun')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_comment', to='posts.comment', verbose_name='Şərh')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='child_comment', to=settings.AUTH_USER_MODEL, verbose_name='İstifadəçi')),
            ],
            options={
                'verbose_name': 'İç-içə şərh',
                'verbose_name_plural': 'İç-içə şərhlər',
                'ordering': ['-created_date'],
            },
        ),
    ]