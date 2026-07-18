from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import SignUpForm, ProfileEditForm


def signup_view(request):
    """
    Create a new account. On success, log the user in right away.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully! Welcome.')
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Login page (uses Django's built-in authentication system).
    """
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'You have logged in successfully.')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """
    Logout.
    """
    next_page = 'core:home'


@login_required
def profile_view(request):
    """
    View and edit the user's profile. Requires login.
    """
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
