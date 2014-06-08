from django.forms import ModelChoiceField

class QuestionModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj['question']