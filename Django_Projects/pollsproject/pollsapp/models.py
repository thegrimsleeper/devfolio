from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    dob = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    published_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text