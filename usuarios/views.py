from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

def login_view(request):
    """Vista personalizada de login"""
    if request.user.is_authenticated:
        return redirect('inventario:dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
            # Redirigir al dashboard después del login exitoso
            next_url = request.GET.get('next', 'inventario:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    """Vista de logout personalizada"""
    if request.method == 'POST' or request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.success(request, f'¡Hasta pronto {username}! Has cerrado sesión correctamente.')
        
        # Redirigir al home después del logout
        return redirect('inventario:home')
    
    return redirect('inventario:home')
