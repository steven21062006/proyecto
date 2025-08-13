from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tienda.models import Producto, Puja, Categoria  # Importación absoluta
from tienda.forms import PujaForm  # Importación absoluta


def lista_productos(request, categoria_slug=None):
    """
    Vista para mostrar la lista de productos, filtrada por categoría si se especifica
    """
    categoria = None
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True)
    
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        productos = productos.filter(categoria=categoria)
    
    context = {
        'categoria': categoria,
        'categorias': categorias,
        'productos': productos,
    }
    return render(request, 'tienda/productos/lista.html', context)

def detalle_producto(request, id, slug):
    """
    Vista para mostrar los detalles de un producto específico
    """
    producto = get_object_or_404(
        Producto,
        id=id,
        slug=slug,
        disponible=True
    )
    
    # Lista de productos relacionados (misma categoría)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        disponible=True
    ).exclude(id=producto.id)[:4]
    
    # Manejo de pujas
    if request.method == 'POST':
        form = PujaForm(request.POST)
        if form.is_valid():
            puja = form.save(commit=False)
            puja.producto = producto
            puja.usuario = request.user
            puja.save()
            
            # Actualizar precio actual del producto
            producto.precio_actual = puja.monto
            producto.save()
            
            messages.success(request, '¡Tu puja ha sido registrada con éxito!')
            return redirect('detalle_producto', id=producto.id, slug=producto.slug)
    else:
        form = PujaForm(initial={'monto': producto.precio_actual + producto.incremento_minimo})
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'form': form,
    }
    return render(request, 'tienda/productos/detalle.html', context)



