import psycopg2
from .models import Authenticate as AuthenticateModel
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import HomePageContent
from django.contrib import messages
from django.core.paginator import Paginator
from axes.decorators import axes_dispatch
from django.db import connections
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def get_db_connection():
    return psycopg2.connect(
        dbname="interoperabilite",
        user="landry",
        password="12345",
        host="localhost"
    )

def home(request):
    content = HomePageContent.objects.first()
    return render(request, 'authentication/home.html', {'content': content})

@axes_dispatch
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Utilisez authenticate ici
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('auth_redirect')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, 'Formulaire invalide. Veuillez réessayer.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def auth_redirect(request):
    if request.user.role == 'director':
        return redirect('dashboard_director')
    elif request.user.role == 'administrateur':
        return redirect('dashboard_admin')
    else:
        return redirect('dashboard_agent')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_director(request):
    return render(request, 'authentication/dashboard_director.html')

@login_required
def dashboard_admin(request):
    return render(request, 'authentication/dashboard_admin.html')

@login_required
def dashboard_agent(request):
    return render(request, 'authentication/dashboard_agent.html')

def is_administrateur(user):
    return user.role == 'administrateur'

@login_required
@user_passes_test(is_administrateur)
def user_list(request):
    with get_db_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM authentication_authenticate")
        columns = [col[0] for col in cursor.description]
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    #paginator = Paginator(users, 10)  # 10 users per page
    #page_number = request.GET.get('page')
    #page_obj = paginator.get_page(page_number)

    print("Columns:", columns)  # Debugging
    print("Users:", users[:2])  # Debugging: print first 2 users
    
    return render(request, 'user_list.html', {'users': users, 'columns': columns})

@login_required
@user_passes_test(is_administrateur)
def user_add(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return render(request, 'authentication/user_add.html')
        
        if AuthenticateModel.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà pris')
            return render(request, 'authentication/user_add.html')
        
        if AuthenticateModel.objects.filter(email=email).exists():
            messages.error(request, 'Cette adresse email est déjà utilisée')
            return render(request, 'authentication/user_add.html')
        
        user = AuthenticateModel.objects.create_user(
            username=username, 
            email=email, 
            password=password1, 
            role=role
        )
        
        messages.success(request, "Compte utilisateur créé avec succès!")
        return redirect('user_list')
    
    return render(request, 'authentication/user_add.html')

@login_required
@user_passes_test(is_administrateur)
@require_POST
def update_user(request):
    data = json.loads(request.body)
    user_id = data.get('id')
    new_data = data.get('data')
    
    user = get_object_or_404(AuthenticateModel, id=user_id)
    for key, value in new_data.items():
        setattr(user, key, value)
    user.save()
    
    return JsonResponse({'status': 'success'})

@login_required
@user_passes_test(is_administrateur)
@require_POST
def delete_user(request):
    data = json.loads(request.body)
    user_id = data.get('id')
    
    user = get_object_or_404(AuthenticateModel, id=user_id)
    user.delete()
    
    return JsonResponse({'status': 'success'})

@login_required
@user_passes_test(lambda u: u.role == 'administrateur')
def user_edit(request, user_id):
    user = get_object_or_404(AuthenticateModel, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur mis à jour avec succès.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'authentication/user_edit.html', {'form': form, 'user': user})

@login_required
@user_passes_test(lambda u: u.role == 'administrateur')
def user_delete(request, user_id):
    user = get_object_or_404(AuthenticateModel, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return JsonResponse({'status': 'success'})
    return render(request, 'authentication/user_delete.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('auth_redirect')
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, 'authentication/edit_profile.html', {'form': form})