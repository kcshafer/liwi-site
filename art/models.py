from django.db import models

class Art(models.Model):
    user = models.ForeignKey('registration.User', blank=True)
    photo = models.ImageField(upload_to='photos/')
    title = models.CharField(max_length=80)
    description = models.TextField()

    class Meta:
        db_table = 'art'