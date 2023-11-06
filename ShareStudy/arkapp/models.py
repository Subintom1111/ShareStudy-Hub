from django.db import models


# Create your models here.
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
) 


COURSE_CHOICES = (
        ("course1", "Course 1"),
        ("course2", "Course 2"),
        ("course3", "Course 3"),
        # Add more course options as needed
    )


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        TEACHER="TEACHER",'Teacher'
        STUDENT="STUDENT",'Student'


    role = models.CharField(max_length=50,choices=Role.choices)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES) 

    course = models.CharField(max_length=10, choices=COURSE_CHOICES)


class Profilete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=12, unique=True)  # You can adjust the max_length as needed
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES) 

    course = models.CharField(max_length=10, choices=COURSE_CHOICES)

    def _str_(self):
        return self.user.username
    
