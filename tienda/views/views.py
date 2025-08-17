from django.shortcuts import render, redirect
from django.contrib import messages
from tienda.models import Producto, Subasta, Categoria
from tienda.forms import ContactoForm  
from django.utils import timezone

def inicio(request):
    """
    Vista para la página de inicio que muestra productos y subastas activas
    """

    
    subastas_activas = Subasta.objects.filter(
        estado='ACTIVA',
        fecha_finalizacion__gt=timezone.now()
    )
    
    return render(request, 'tienda/inicio.html', {
        
        'subastas_activas': subastas_activas
    })

def acerca_de(request):
    """
    Vista para la página 'Acerca de'
    """
    return render(request, 'tienda/acerca_de.html')

def contacto(request):
    """
    Vista para la página de contacto con formulario funcional
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Mensaje enviado con éxito!')
            return redirect('contacto')
    else:
        form = ContactoForm()
    
    return render(request, 'tienda/contacto.html', {
        'form': form
    })

def lista_categorias(request):
    """
    Vista para mostrar todas las categorías disponibles
    """
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categorias/lista.html', {
        'categorias': categorias
    })

def moto(request):
    return render(request, 'tienda/subastas/moto.html')


from django.shortcuts import render
from django.utils import timezone
from tienda.models import Subasta

def lista_categoria(request, categoria):
    subastas = Subasta.objects.filter(
        producto__categoria__nombre__icontains=categoria,
        estado='ACTIVA',
        fecha_finalizacion__gt=timezone.now()
    ).order_by('-fecha_inicio')

    return render(request, 'tienda/subastas/lista_categoria.html', {
        'subastas': subastas,
        'categoria_nombre': categoria.replace('-', ' ').capitalize()
    })



