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


class Category(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=255)
    duration = models.DurationField(blank=True)
    quiz_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Question(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='questions')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if self.id is None:
            self.category.quiz_count += 1
            self.category.save()

    def delete(self, *args, **kwargs):
        obj = super().delete(*args, **kwargs)
        self.category.quiz_count -= 1
        self.category.save()


class Variant(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='variants')
    title = models.CharField(max_length=255)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Result(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    score = models.PositiveIntegerField(default=0)
    success = models.PositiveIntegerField(default=0)
    fail = models.PositiveIntegerField(default=0)
    end = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.success} {self.fail}'

    def user_info(self):
        return f"{self.user.username} {self.user.last_name}"


class QuestionResult(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='question_results')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='correct_answers')
    selected_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='selected_answers')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Result for {self.result.user.username} in {self.question.title}"
    


class MainPage(models.Model):
    logo = models.ImageField(default='logo.jpg', upload_to='site-logo')
    facebook = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.phone
     