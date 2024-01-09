""" Module for user-related forms and models.
This module defines forms and models for managing user data, including user registration,
profile updates, and account details. It leverages Django's authentication system and ORM.

Key classes:
    - UserRegisterForm: Form for new user registration with password confirmation and email verification.
    - UserUpdateForm: Form for updating existing user accounts (username and email).
    - ProfileUpdateForm: Form for updating user profile information, including image uploads.
Dependencies:
    - forms module from Django for creating form classes.
    - User and models module from Django for defining the User model.
    - Image, BytesIO, and ImageField from PIL (Python Imaging Library)"""
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

STATES = [
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming'),
]


class UserRegisterForm(UserCreationForm):
    """Form for registering new users with password confirmation and email verification.

    This form inherits from `UserCreationForm` provided by Django and adds
    the following fields:
    * `username`: A `CharField` for entering the desired username. Do I neeed this
    * `email`: An `EmailField` instance for collecting user email addresses.
    * `password1`: A `CharField` instance for entering the password.
    * `password2`: A `CharField` instance for confirming the password.
    * `firstname`: A `CharField` for entering the user's first name.
    * `lastname`: A `CharField` for entering the user's last name.
    * `address_1`: A `CharField` for entering the user's primary address.
    * `address_2`: A `CharField` for entering additional address details (apartment, studio, floor).
    * `city`: A `CharField` for entering the city.
    * `state`: A `ChoiceField` for selecting the state from a predefined list.
    * `zip_code`: A `CharField` for entering the ZIP code.
    * `phone`: An `IntegerField` for entering the phone number.

    Raises:
        ValidationError: If the passwords entered in `password1` and `password2`
            fields do not match.
    Returns:
        A valid `UserRegisterForm` instance containing the submitted user data.

    """

    # need to add more fields like, firstname, lastname,
    # username = forms.CharField(label='Username', required=True, max_length=100) # might not need this. 
    firstname = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    lastname = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=True)
    email = forms.EmailField(label="Please enter your email address", required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=15)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, min_length=15)
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(label='State', choices=STATES) 
    zip_code = forms.CharField(label='Zip')
    phone = forms.IntegerField(blank=True, default=None, min_length=10, max_length=10)

    class Meta:
        """Configures the model and fields for the UserRegisterForm.
        
        Attributes:
            model: Specifies the User model as the basis for the form.
            fields: Lists the fields to include in the form: username, email, password1, password2.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'firstname', 'lastname', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'phone' ]

    def clean_password2(self):
        """Validates that the two password fields match.
        This method checks if the values entered in the `password1` and
        `password2` fields are identical. If they are not, it raises a
        `ValidationError` with a helpful message.

        Returns:
            The confirmed password if valid, otherwise raises a ValidationError.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2



    def save(self, commit=True):
        """Saves the user, sets their email address, and sends a verification email.

        This method overrides the base `save` method to additionally set the
        user's email address and send a verification email after saving the
        user to the database.

        Args:
            commit: Whether to commit the user to the database (True by default).

        Returns:
            The saved user object.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Assuming a function for sending verification email in utils.py
            user.send_verification_email()  
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating existing user accounts.

    Inherits from `forms.ModelForm` and is based on the `User` model.
    Provides fields for updating various user details.

    Key features:
    - Inherits validation logic for username and email fields from the model.
    - Doesn't include password fields for security reasons.

    Attributes:
        firstname: The user's first name.
        lastname: The user's last name.
        email: The user's email address.
        address_1: The user's address line 1.
        address_2: The user's address line 2.
        city: The user's city.
        state: The user's state.
        zip_code: The user's zip code.
        phone: The user's phone number.
"""
    firstname = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    lastname = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=True)
    email = forms.EmailField(label="Please enter your email address", required=True)
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(label='State', choices=STATES)
    zip_code = forms.CharField(label='Zip')
    phone = forms.IntegerField(null=True, min_length=10, max_length=10)
    class Meta:
        """Configures the model and fields for the UserUpdateForm.
        - model: Specifies the User model as the basis for the form.
        - fields: Lists the fields to include in the form: username and email.
        """
        model = User
        fields = ['username', 'email', 'firstname', 'lastname', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'phone' ]

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile information.

This form inherits from `forms.ModelForm` and is based on the `Profile` model.
It provides a field for:

- image: The user's profile image (for uploading).

Key features:

- Handles image uploads using Django's file handling mechanisms.
- Uses the `ImageField` to store the profile image in the database.
"""
    class Meta:
        """Configures the model and fields for the ProfileUpdateForm.
        - model: Specifies the Profile model as the basis for the form.
        - fields: Lists the field to include in the form: image.
        """
        model = Profile
        fields = ["image"]