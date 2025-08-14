from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tienda.forms import CustomUserCreationForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tienda:inicio')
        messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'tienda/registration/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('tienda:inicio')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tienda:inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tienda/registration/registro.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('tienda:inicio')
