from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser, UserActivity
from django.contrib import messages
from django_otp.decorators import otp_required
from two_factor.views import LoginView, SetupView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method=['GET', 'POST'], block=True)
class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'

class CustomSetupView(SetupView):
    template_name = 'authentication/setup_2fa.html'
    success_url = reverse_lazy('two_factor:setup_complete')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'authentication/password_change.html'
    success_url = reverse_lazy('password_change_done')

@ratelimit(key='ip', rate='5/m', method=['GET', 'POST'], block=True)
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie. Bienvenue!')
            return redirect('two_factor:setup')
        else:
            messages.error(request, 'Erreur lors de l\'inscription. Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

@otp_required
@login_required
@user_passes_test(lambda u: u.is_director())
def dashboard_director_view(request):
    return render(request, 'authentication/dashboard_director.html')

@otp_required
@login_required
@user_passes_test(lambda u: u.is_admin())
def dashboard_admin_view(request):
    return render(request, 'authentication/dashboard_admin.html')

@otp_required
@login_required
@user_passes_test(lambda u: u.is_agent())
def dashboard_agent_view(request):
    return render(request, 'authentication/dashboard_agent.html')

def log_user_activity(request, activity_type):
    UserActivity.objects.create(
        user=request.user,
        activity_type=activity_type,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

def home(request):
    return render(request, 'home.html')
