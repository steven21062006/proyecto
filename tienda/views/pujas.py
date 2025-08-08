from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tienda.models import Puja, Producto  # Importación absoluta desde tienda.models
from tienda.forms import PujaForm  # Importación absoluta desde tienda.forms

@login_required
def hacer_puja(request, producto_id):
    """
    Vista para manejar el proceso de hacer una puja en un producto
    """
    producto = get_object_or_404(Producto, id=producto_id, disponible=True)
    
    if request.method == 'POST':
        form = PujaForm(request.POST)
        if form.is_valid():
            try:
                # Crear la puja pero no guardarla aún
                puja = form.save(commit=False)
                puja.usuario = request.user
                puja.producto = producto
                
                # Validar que la puja sea mayor que el precio actual
                if puja.monto <= producto.precio_actual:
                    messages.error(request, 'El monto debe ser mayor al precio actual')
                    return redirect('detalle_producto', producto_id=producto.id)
                
                # Guardar la puja y actualizar el producto
                puja.save()
                producto.precio_actual = puja.monto
                producto.save()
                
                messages.success(request, '¡Puja realizada con éxito!')
                return redirect('detalle_producto', producto_id=producto.id)
            
            except Exception as e:
                messages.error(request, f'Error al procesar la puja: {str(e)}')
    else:
        # Inicializar el formulario con el monto mínimo requerido
        form = PujaForm(initial={'monto': producto.precio_actual + producto.incremento_minimo})
    
    context = {
        'producto': producto,
        'form': form,
    }
    return render(request, 'tienda/pujas/hacer_puja.html', context)

@login_required
def mis_pujas(request):
    """
    Vista para mostrar el historial de pujas del usuario actual
    """
    pujas = Puja.objects.filter(usuario=request.user).select_related('producto').order_by('-fecha')
    return render(request, 'tienda/pujas/mis_pujas.html', {'pujas': pujas})



