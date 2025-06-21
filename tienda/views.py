from django.shortcuts import render, redirect

def landing(request):
    # Carga los productos guardados en sesión (o lista vacía si no hay)
    productos = request.session.get('productos', [])
    context = {'productos': productos}
    return render(request, 'tienda/landing.html', context)

def formulario(request):
    if request.method == 'POST':
        # Obtener productos guardados en sesión
        productos = request.session.get('productos', [])

        # Crear nuevo producto con datos del formulario
        producto = {
            'id': request.session.get('next_id', 1),
            'name': request.POST.get('productName'),
            'category': request.POST.get('productCategory'),
            'brand': request.POST.get('productBrand'),
            'size': request.POST.get('productSize'),
            'color': request.POST.get('productColor'),
            'price': float(request.POST.get('productPrice', 0)),
            'quantity': int(request.POST.get('productQuantity', 0)),
            'description': request.POST.get('productDescription'),
        }

        # Añadir producto a la lista
        productos.append(producto)

        # Guardar la lista actualizada en sesión
        request.session['productos'] = productos

        # Actualizar el siguiente ID
        request.session['next_id'] = producto['id'] + 1

        # Redirigir a inventario
        return redirect('landing')

    # Si es GET, mostrar formulario
    return render(request, 'tienda/formulario.html')

def listado(request):
    productos = request.session.get('productos', [])
    context = {'productos': productos}
    return render(request, 'tienda/listado.html', context)

