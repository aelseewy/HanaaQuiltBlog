from django import forms
from .models import SignUp

class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Enter your email address",
        "aria-label":"email address",
        "aria-describedby": "button-addon2",
    }), label="" )
    class Meta:
        model = SignUp
        fields = ('email', )
