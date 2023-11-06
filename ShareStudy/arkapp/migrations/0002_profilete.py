# Generated by Django 3.0.5 on 2023-10-29 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arkapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profilete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=12, unique=True)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=10)),
                ('course', models.CharField(choices=[('course1', 'Course 1'), ('course2', 'Course 2'), ('course3', 'Course 3')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]