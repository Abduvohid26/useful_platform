from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import validate_image


class User(AbstractUser):
    pass


class Welcome(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField()
    image = models.FileField(upload_to='welcome-images', validators=[validate_image])

    def __str__(self):
        return self.name


class AboutPlatform(models.Model):
    body = models.TextField()
    boyd1 = models.TextField()
    image = models.FileField(upload_to='welcome-images', validators=[validate_image])
    author = models.CharField(max_length=255)
    author_image = models.FileField(upload_to='auhtor-images', validators=[validate_image])

    def __str__(self):
        return self.author


class Directions(models.Model):
    name = models.CharField(max_length=255)
    user_qty = models.IntegerField()
    subject_qty = models.IntegerField()
    material_qty = models.IntegerField()
    image = models.ImageField(upload_to='directions-image')
    body = models.TextField()

    def __str__(self):
        return self.name


class Sciences(models.Model):
    directions = models.ForeignKey(Directions, on_delete=models.CASCADE, related_name='sciences')
    body = models.TextField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)
    sciences = models.ForeignKey(Sciences, on_delete=models.CASCADE, related_name='subject')

    def __str__(self):
        return self.name


class Problems(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    video = models.FileField(upload_to='subject-video')
    body = models.TextField()
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.body[:50]


class ProblemImages(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE, related_name='problems')
    image = models.FileField(upload_to='problem-images')

    def __str__(self) -> str:
        return f'{self.problem.name}'


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name

