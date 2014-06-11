from django.db import models

def upload_to(instance, filename):
    return 'art/%s/%s' % (instance.user.id, filename)

class Art(models.Model):
    user = models.ForeignKey('registration.User', blank=True)
    photo = models.ImageField(upload_to=upload_to)
    title = models.CharField(max_length=80)
    description = models.TextField()

    class Meta:
        db_table = 'art'

class Like(models.Model):
    user = models.ForeignKey('registration.User')
    art = models.ForeignKey('art.Art')
    art_user_like = models.CharField(max_length=80)
    
    class Meta:
        db_table = 'art_like'