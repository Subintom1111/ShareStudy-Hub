# Generated by Django 3.0.5 on 2023-11-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arkapp', '0007_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('assigned_teachers', models.CharField(max_length=255)),
                ('credit_hours', models.PositiveIntegerField()),
                ('course_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('available_seats', models.PositiveIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]