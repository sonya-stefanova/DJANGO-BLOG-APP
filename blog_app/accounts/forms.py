from django import forms
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.forms import EmailField
from setuptools._entry_points import _

from blog_app.accounts.models import Profile

UserModel = get_user_model()


class BlogAppUserCreationForm(auth_forms.UserCreationForm):

    first_name = forms.CharField(
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        max_length=30,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _('It works')
        self.fields['password2'].help_text = _('It works')


    def save(self, commit=True):
        user = super().save(commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
        )

        if commit:
            profile.save()

        return user


    class Meta(auth_forms.UserCreationForm):
        model = UserModel
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')
        field_classes = {"email": EmailField}


class CustomSignInForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    error_messages = {
        'invalid_login': f"Please enter a correct {'username'}s and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    labels = {
        'email': '',
        'password': '',}

class BlogAppUserChangeForm(auth_forms.UserChangeForm):

    class Meta:
        model = UserModel
        fields = ("email",)



class BlogAppPasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                'class': 'form-control',
                "placeholder": "Fill in your Old password",
            }
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": 'form-control',
                "placeholder": "Fill in your New password",

            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("Confirm your password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": 'form-control',
                "placeholder": "Confirm your New password",
            }
        ),
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('slug', 'user')

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Change your first name',
                    'class': 'form-control',

                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Change your last name',
                    'class': 'form-control',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'placeholder': 'Enter an updated bio',
                    'class': 'form-control',

                },
            ),
        }

        labels = {
            'first_name': '',
            'last_name': '',
            'image': '',
            'bio': '',
        }

