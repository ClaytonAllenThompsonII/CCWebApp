from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login


# Create your views here.

def register(request):
    """Handles user registration requests. This view processes POST requests containing user registration data,
    validates the data using the `UserRegisterForm`, and takes the following actions:

    * If the form is valid, saves the user, sends a verification email, and displays
      a success message with instructions for email verification.
    * If the form is invalid, displays the form again with error messages highlighting
      any invalid fields.

    Args:
        request: The Django HTTP request object.

    Returns:
        An HTTP response object corresponding to the rendered registration page
        or the login page after successful registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! A verification email has been sent to your inbox. Please verify your email to log in.')
            return redirect('login')
        else:
            messages.error(request, 'There were errors in your registration form. Please check the highlighted fields and try again.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def verify_email(request, verification_code): #email verification logic using code to activate user's account. 
    """Verifies a user's email using the provided verification code.
    Args:
        request: The Django HTTP request object.
        verification_code: The verification code from the email link.
    Returns:
        An HTTP response object corresponding to the success message or error page.
    """
    User = get_user_model()  # Get the User model
    try:
        user = User.objects.get(verification_code=verification_code)
        user.is_active = True
        user.verification_code = ''
        user.save()
        update_last_login(None, user)  # Update last login
        messages.success(request, 'Your email has been verified! You are now able to log in.')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification code.')
        return redirect('register')  # Or redirect to a dedicated error page

