from django import forms
from django.forms import modelformset_factory
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )

    class Meta:
        model = Choice
        fields = ['choice_text']

ChoiceFormSet = modelformset_factory(
    Choice,
    form=ChoiceForm,
    extra=3  # Start with 3 empty forms
)