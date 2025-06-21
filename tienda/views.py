from django.shortcuts import render, redirect

def landing(request):
    # Aquí cargas los productos desde tu base de datos o contexto
    productos = []  # ejemplo: carga real de productos
    context = {'productos': productos}
    return render(request, 'tienda/landing.html', context)

def formulario(request):
    if request.method == 'POST':
        # Aquí procesas los datos del formulario para guardar producto
        # Luego rediriges al inventario
        return redirect('landing')
    return render(request, 'tienda/formulario.html')

def listado(request):
    # Puedes usar esta vista para mostrar todos los productos si quieres
    productos = []  # ejemplo
    context = {'productos': productos}
    return render(request, 'tienda/listado.html', context)
