from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tienda.models import Puja  




@login_required
def mis_pujas(request):
    """
    Vista para mostrar el historial de pujas del usuario actual
    """
    pujas = Puja.objects.filter(usuario=request.user).select_related('producto').order_by('-fecha')
    return render(request, 'tienda/pujas/mis_pujas.html', {'pujas': pujas})



