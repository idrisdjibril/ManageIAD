from django.contrib.auth import get_user_model
from django import forms
from .models import Message, Tag

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=get_user_model().objects.all())  # Correctly use get_user_model
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.none(), required=False)

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body', 'attachment', 'tags']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
