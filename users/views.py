from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


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


def verify_email(request, verification_code):
    """Verifies a user's email using the provided verification code.
    Args:
        request: The Django HTTP request object.
        verification_code: The verification code from the email link.
    Returns:
        An HTTP response object corresponding to the success message or error page.
    """
    Profile = get_user_model()  # Get the User model
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

@login_required
def profile(request):
    """Handles user profile viewing and updating requests.

This view serves two primary purposes:

1. **GET requests**: Renders the profile page, displaying the user's current
   information and forms for updating their profile and account details.
2. **POST requests**: Processes form submissions for updating the user's profile
   and account information. If validation is successful, saves the updated
   data and redirects to the profile page with a success message.

Key actions:

- Retrieves and instantiates UserUpdateForm and ProfileUpdateForm.
- Handles form validation and saving upon successful POST requests.
- Renders the `users/profiles.html` template with relevant context data.

Requires authentication: This view requires a logged-in user to access.
"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.users)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profiles.html', context)