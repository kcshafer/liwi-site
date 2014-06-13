from django.forms import ModelChoiceField

class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj['name']