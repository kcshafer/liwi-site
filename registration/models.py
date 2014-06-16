from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_artist = models.BooleanField()
    type = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)

    class Meta:
        db_table = 'user'

class SecurityQuestion(models.Model):
    question = models.CharField(max_length = 250, null=False)

    class Meta:
        db_table = 'secret_question'
        
class SecurityAnswer(models.Model):
    user = models.ForeignKey(User)
    security_questions = models.ForeignKey(SecurityQuestion)
    answer = models.CharField(max_length = 250, null=False)

    class Meta:
        db_table = 'secret_answer'

