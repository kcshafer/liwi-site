from django.db import models

class Profile(models.Model):
    user = models.ForeignKey('registration.User')
    bio = models.TextField(blank=True, null=True)
    twitter = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        db_table = 'user_profile'