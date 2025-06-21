from django.shortcuts import render, redirect

def landing(request):
    # Renderiza la plantilla landing.html dentro de tienda/templates/tienda/
    return render(request, "tienda/landing.html")

def formulario(request):
    # Renderiza el formulario para agregar productos
    return render(request, "tienda/formulario.html")

def listado(request):
    # Renderiza el listado o edición de productos
    return render(request, "tienda/lisatdo.html")