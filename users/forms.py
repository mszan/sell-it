# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm
from django_registration.forms import RegistrationForm
from django.contrib.auth.models import User
from crispy_forms.layout import Layout, Fieldset

from offers.forms import resize_uploaded_image
from users.models import UserProfile


class UserRegisterForm(RegistrationForm):
    """
    Form used to register new users.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Fieldset('Register', 'username', 'email', 'password1', 'password2'),)

        help_text_class = 'text-dark'
        self.fields['username'].help_text = f'<span class="{help_text_class}">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>'
        self.fields['password1'].help_text = f"""
            <ul class="{help_text_class}">
                <li>Your password can’t be too similar to your other personal information.</li>
                <li>Your password must contain at least 8 characters.</li>
                <li>Your password can’t be a commonly used password.</li>
                <li>Your password can’t be entirely numeric.</li>
            </ul>
        """
        self.fields['password2'].help_text = f'<span class="{help_text_class}">Enter the same password as before, for verification.</span>'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    """
    Form used to login registered users.
    """
    class Meta:
        model = User
        fields = ['username', 'password']


class UserEditForm(forms.ModelForm):
    """
    Form used to edit user's information.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileEditForm(forms.ModelForm):
    """
    Form used to edit user profile's information.
    """
    image_width = 300
    image_height = 300

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'voivodeship', 'phone_number', 'phone_number_visible']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'custom-file-input',
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
            })
        }

    def clean_profile_picture(self):
        """
        Scale down profile picture.
        :return: scaled down image.
        """
        image = self.cleaned_data.get('profile_picture')
        image = resize_uploaded_image(image, self.image_width, self.image_height)
        return image
