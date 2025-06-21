from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')

def formulario(request):
    return render(request, 'formulario.html')

def listado(request):
    return render(request, 'listado.html')