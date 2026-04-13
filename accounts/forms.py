# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Rule: Only letters allowed (prevents random gibberish like 'name123_!!')
alpha_validator = RegexValidator(
    r'^[a-zA-Z]+$', 
    "Only plain letters are allowed. No numbers or symbols."
)

class StrictRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        min_length=5, 
        max_length=15, 
        validators=[alpha_validator],
        help_text="5-15 characters. Letters only."
    )
    
    first_name = forms.CharField(validators=[alpha_validator], required=True)
    last_name = forms.CharField(validators=[alpha_validator], required=True)

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    # Custom logic to prevent "random" long strings in passwords
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 32:
            raise ValidationError("Password is too long (Max 32 characters).")
        return password