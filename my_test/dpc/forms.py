from django import forms
from models import DPCData, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')


class DPCForm(forms.ModelForm):

    class Meta:
        model = DPCData
        fields = ('title', 'notes', 'parameter1', 'parameter2')
