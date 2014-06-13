from django.forms import ModelChoiceField, ModelMultipleChoiceField

from art.models import Tag


class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj['name']


class TagModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj[0]

    def clean(self, value):
        try:
            return Tag.objects.get(name=value)
        except:
            pass