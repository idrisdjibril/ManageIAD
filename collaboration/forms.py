from django import forms
from .models import Message, Attachment
from ckeditor.widgets import CKEditorWidget

class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body', 'tags']

class MessageSearchForm(forms.Form):
    query = forms.CharField(label='Rechercher', max_length=100)
    search_in = forms.ChoiceField(choices=[('subject', 'Sujet'), ('body', 'Corps'), ('tags', 'Tags')])