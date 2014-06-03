from django.db import models

class Profile(models.Model):
    user = models.ForeignKey('registration.User')
    bio = models.TextField()
    twitter = models.CharField(max_length=80)

    class Meta:
        db_table = 'user_profile'