from django import forms
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Ensure email field is always required

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

