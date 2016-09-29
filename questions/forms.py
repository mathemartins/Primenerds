from django import forms
from questions.models import Question

#class QuestionForm(forms.ModelForm):
#    """docstring for QuestionForm"""
#    class Meta:
#        model = Question
#        fields = ['user', 'destination', 'text']

class QuestionForm(forms.Form):
    """docstring for QuestionForm"""
    question = forms.CharField(label='', widget=forms.Textarea(attrs={"placeholder": "add your comments or replies"}))
