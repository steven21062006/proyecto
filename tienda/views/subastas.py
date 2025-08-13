from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

from tienda.models import Producto, Puja, ComentarioMoto, Subasta
from tienda.forms import SubastaForm, PujaForm, MultipleImagenSubastaForm




def procesar_comentario_subasta(request, slug):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', '').strip()
            if not texto:
                return JsonResponse({'success': False, 'message': 'El comentario no puede estar vacío'}, status=400)

            # Buscar la subasta por slug
            subasta = get_object_or_404(Subasta, slug=slug)
            producto = subasta.producto

            # Crear comentario asociado al producto
            nuevo_comentario = ComentarioMoto.objects.create(
                producto=producto,
                usuario=request.user,
                comentario=texto,
                fecha=timezone.now()
            )

            return JsonResponse({
                'success': True,
                'nuevo_comentario': {
                    'usuario': nuevo_comentario.usuario.username,
                    'comentario': nuevo_comentario.comentario,
                    'fecha': nuevo_comentario.fecha.strftime("%d/%m/%Y %H:%M")
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)




def lista_subastas(request):
    subastas = Subasta.objects.filter(
        estado='ACTIVA',
        fecha_finalizacion__gt=timezone.now()
    ).order_by('-fecha_creacion')

    return render(request, 'tienda/subastas/lista_subastas.html', {
        'subastas': subastas
    })


#@login_required(login_url='tienda:login')
def detalle_subasta(request, slug):
    subasta = get_object_or_404(Subasta, slug=slug)
    puja_form = None

    # Solo permitir pujar si está activa y el usuario no es el creador
    if subasta.estado == 'ACTIVA' and subasta.usuario != request.user:
        if request.method == 'POST':
            puja_form = PujaForm(request.POST, subasta=subasta)
            if puja_form.is_valid():
                puja = puja_form.save(commit=False)
                if puja.monto <= subasta.precio_actual:
                    messages.error(request, f'El monto debe ser mayor al precio actual (${subasta.precio_actual})')
                else:
                    puja.subasta = subasta
                    puja.usuario = request.user
                    puja.save()
                    subasta.precio_actual = puja.monto
                    subasta.save()
                    messages.success(request, '¡Puja realizada con éxito!')
                    return redirect('tienda:detalle_subasta', slug=subasta.slug)
        else:
            puja_form = PujaForm(subasta=subasta)
    else:
        # Si no puede pujar, no mostrar formulario
        puja_form = None

    pujas = subasta.pujas.all().order_by('-fecha')

    return render(request, 'tienda/subastas/detalle_subasta.html', {
        'subasta': subasta,
        'pujas': pujas,
        'puja_form': puja_form,
        'puja_actual': subasta.precio_actual,
        'total_pujas': pujas.count(),
        'usuario_autenticado': request.user.is_authenticated,
    })


@login_required
def crear_subasta(request):
    if request.method == 'POST':
        subasta_form = SubastaForm(request.POST, request.FILES)
        imagenes_form = MultipleImagenSubastaForm(request.POST, request.FILES)

        if subasta_form.is_valid() and imagenes_form.is_valid():
            subasta = subasta_form.save(commit=False)
            subasta.usuario = request.user
            subasta.precio_actual = subasta.precio_inicial
            subasta.save()

            
                

            messages.success(request, '¡Subasta creada con éxito!')
            return redirect('detalle_subasta', slug=subasta.slug)
    else:
        subasta_form = SubastaForm()
        imagenes_form = MultipleImagenSubastaForm()

    return render(request, 'tienda/subastas/crear_subasta.html', {
        'subasta_form': subasta_form,
        'imagenes_form': imagenes_form
    })


@login_required
def mis_subastas(request):
    subastas = Subasta.objects.filter(
        usuario=request.user
    ).order_by('-fecha_creacion')

    return render(request, 'tienda/subastas/mis_subastas.html', {
        'subastas': subastas
    })


@login_required
def finalizar_subasta(request, slug):
    subasta = get_object_or_404(Subasta, slug=slug, usuario=request.user)

    if subasta.estado == 'ACTIVA':
        subasta.estado = 'FINALIZADA'

        ultima_puja = subasta.pujas.order_by('-monto').first()
        if ultima_puja:
            subasta.ganador = ultima_puja.usuario

        subasta.save()
        messages.success(request, 'Subasta finalizada correctamente')
    else:
        messages.warning(request, 'La subasta ya estaba finalizada')

    return redirect('detalle_subasta', slug=subasta.slug)



