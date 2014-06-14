from django.db import models

def upload_to(instance, filename):
    return 'user/%s/%s' % (instance.user.id, filename)

class Profile(models.Model):
    user = models.ForeignKey('registration.User')
    bio = models.TextField(blank=True, null=True)
    twitter = models.CharField(max_length=80, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to, null=True)

    class Meta:
        db_table = 'user_profile'