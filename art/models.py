from django.db import models
from django import template

register = template.Library()

def upload_to(instance, filename):
    return 'art/%s/%s' % (instance.user.id, filename)

class Art(models.Model):
    user = models.ForeignKey('registration.User', blank=True)
    category = models.ForeignKey('art.Category', blank=True, null=True)
    photo = models.ImageField(upload_to=upload_to)
    title = models.CharField(max_length=80)
    description = models.TextField()
    category = models.CharField(max_length=80)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'art'

    @register.tag(name="get_tags")
    def get_tags(self):
        tags = ArtTag.objects.filter(art__id=self.id).values('tag__name')
        return ' '.join([t.get('tag__name') for t in tags])

class Like(models.Model):
    user = models.ForeignKey('registration.User')
    art = models.ForeignKey('art.Art')
    art_user_like = models.CharField(max_length=80)

    class Meta:
        db_table = 'art_like'

class Category(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        db_table = 'category'

class Tag(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        db_table = 'tag'

class ArtTag(models.Model):
    art = models.ForeignKey('art.Art')
    tag = models.ForeignKey('art.Tag')

    class Meta:
        db_table = 'art_tag'
