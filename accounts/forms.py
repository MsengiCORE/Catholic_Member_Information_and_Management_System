from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    """
    Custom login form for CCMIMS.
    """

    username = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Enter your phone number",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full pr-12",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )


class CompleteRegistrationForm(forms.Form):
    """
    Form used by a newly registered church member
    to create their login account.
    """

    phone_number = forms.CharField(
        label="Phone Number",
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full bg-white",
                "placeholder": "Enter your phone number",
                "autocomplete": "tel",
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full bg-white",
                "placeholder": "Create your password",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full bg-white",
                "placeholder": "Confirm your password",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"].strip()

        allowed_characters = "0123456789+ -()"

        if any(
            char not in allowed_characters
            for char in phone_number
        ):
            raise forms.ValidationError(
                "Phone number contains invalid characters."
            )

        if User.objects.filter(username=phone_number).exists():
            raise forms.ValidationError(
                "This phone number is already registered."
            )

        return phone_number

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "Passwords do not match."
            )

        return cleaned_data