from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
#from captcha.fields import ReCaptchaField

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    phone_number = forms.CharField(max_length=15, required=False)
    department = forms.CharField(max_length=100, required=False)
    #captcha = ReCaptchaField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'user_type', 'phone_number', 'department')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError(_("Le mot de passe doit contenir au moins 8 caractères."))
        if not any(char.isdigit() for char in password1):
            raise ValidationError(_("Le mot de passe doit contenir au moins un chiffre."))
        if not any(char.isupper() for char in password1):
            raise ValidationError(_("Le mot de passe doit contenir au moins une lettre majuscule."))
        return password1

class CustomAuthenticationForm(AuthenticationForm):
    #captcha = ReCaptchaField()

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(_("Ce compte est inactif."), code='inactive')