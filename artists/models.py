from django.db import models

class FeaturedArtist(models.Model):
    user = models.ForeignKey('registration.User', blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    last_imprint = models.DateTimeField()
    total_imprints = models.IntegerField()
    active = models.BooleanField()
    photo = models.CharField(max_length=100)

    class Meta:
        db_table = 'featured_artist'