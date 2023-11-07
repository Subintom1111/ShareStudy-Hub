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
    




from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    assigned_teachers = models.CharField(max_length=200)





from django.db import models

class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



from django.db import models

class ExamMark(models.Model):
    course_name = models.CharField(max_length=100)
    question_number = models.IntegerField()
    total_marks = models.IntegerField()
    exam_time = models.CharField(max_length=20)  # Add the exam_time field


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)


class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the student who made the submission
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)  # Link to the assignment
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the submission was made
    document = models.FileField(upload_to='submissions/')  # Upload a file as the submission
