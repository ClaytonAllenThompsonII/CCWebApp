from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """Form for registering new users with password confirmation and email verification.

    This form inherits from `UserCreationForm` provided by Django and adds
    the following fields:
    * `email`: An email address field for user contact and verification.
    * `password2`: A password confirmation field to ensure password accuracy.

    The form also overrides the following methods:
    * `clean_password2`: Validates that the two password fields match.
    * `save`: Saves the user, sets their email address, and sends a verification email.

    Args:
        *args: Arguments for the base `UserCreationForm` constructor.
        *kwargs: Keyword arguments for the base `UserCreationForm` constructor.

    Attributes:
        email: An `EmailField` instance for collecting user email addresses.
        password1: A `CharField` instance for entering the password.
        password2: A `CharField` instance for confirming the password.

    Raises:
        ValidationError: If the passwords entered in `password1` and `password2`
            fields do not match.

    Returns:
        A valid `UserRegisterForm` instance containing the submitted user data.
    """

    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
            user.send_verification_email()  # Assuming a function for sending verification email in utils.py
        return user