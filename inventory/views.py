from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.

def register(request):
    """Handles user registration.

    Receives a POST request with user registration data, validates it,
    creates a new user account, and redirects to the login page upon success.
    If the request method is not POST, renders an empty registration form.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Renders the registration page or redirects to the login page.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})