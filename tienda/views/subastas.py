from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tienda.models import Subasta, Puja, ImagenSubasta  # Import absoluto
from tienda.forms import SubastaForm, PujaForm, MultipleImagenSubastaForm  # Import absoluto
import json
from django.http import JsonResponse

def detalle_auto_deportivo(request):
    # Datos estáticos para el auto deportivo
    context = {
        'user': request.user,
        'subasta': {
            'titulo': 'Auto Deportivo de Lujo',
            'descripcion': 'Vehículo exclusivo - Edición Limitada',
            'precio_inicial': 25000,
            'fecha_fin': '2023-12-31 23:59:59',
            'slug': 'auto-deportivo'
        }
    }
    return render(request, 'tienda/subastas/detalle_auto_deportivo.html', context)

@login_required
def procesar_puja_auto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto'))
            
            # Aquí iría la lógica para guardar en base de datos
            # Ejemplo simplificado:
            nueva_puja = {
                'usuario': request.user.username,
                'monto': monto,
                'fecha': timezone.now().strftime("%d/%m/%Y %H:%M")
            }
            
            return JsonResponse({
                'success': True,
                'nueva_puja': nueva_puja
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)


#apple watch
def apple_watch(request):
    # Datos estáticos para el auto deportivo
    context = {
        'user': request.user,
        'subasta': {
            'titulo': 'Apple Watch Series 9',
            'descripcion': 'Reloj exclusivo - Edición Limitada',
            'precio_inicial': 25000,
            'fecha_fin': '2023-12-31 23:59:59',
            'slug': 'apple-watch'
        }
    }
    return render(request, 'tienda/subastas/apple_watch.html', context)

@login_required
def procesar_puja_apple(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto'))
            
            # Aquí iría la lógica para guardar en base de datos
            # Ejemplo simplificado:
            nueva_puja = {
                'usuario': request.user.username,
                'monto': monto,
                'fecha': timezone.now().strftime("%d/%m/%Y %H:%M")
            }
            
            return JsonResponse({
                'success': True,
                'nueva_puja': nueva_puja
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=405)


def lista_subastas(request):
    subastas = Subasta.objects.filter(
        estado='ACTIVA',
        fecha_finalizacion__gt=timezone.now()
    ).order_by('-fecha_creacion')
    
    return render(request, 'tienda/subastas/lista_subastas.html', {
        'subastas': subastas
    })

# ... (resto del código permanece igual)

def detalle_subasta(request, slug):
    """
    Vista para mostrar el detalle de una subasta y manejar pujas
    """
    subasta = get_object_or_404(Subasta, slug=slug)
    puja_form = None
    
    # Solo mostrar formulario de puja si está activa y el usuario no es el dueño
    if subasta.estado == 'ACTIVA' and subasta.usuario != request.user:
        if request.method == 'POST':
            puja_form = PujaForm(request.POST, subasta=subasta)
            if puja_form.is_valid():
                puja = puja_form.save(commit=False)
                puja.subasta = subasta
                puja.usuario = request.user
                puja.save()
                
                # Actualizar precio actual de la subasta
                subasta.precio_actual = puja.monto
                subasta.save()
                
                messages.success(request, '¡Puja realizada con éxito!')
                return redirect('detalle_subasta', slug=subasta.slug)
        else:
            puja_form = PujaForm(subasta=subasta)
    
    # Obtener imágenes adicionales e historial de pujas
    imagenes = subasta.imagenes_adicionales.all().order_by('orden')
    pujas = subasta.pujas.all().order_by('-fecha')
    
    return render(request, 'tienda/subastas/detalle_subasta.html', {
        'subasta': subasta,
        'imagenes': imagenes,
        'pujas': pujas,
        'puja_form': puja_form
    })

@login_required
def crear_subasta(request):
    """
    Vista para crear una nueva subasta
    """
    if request.method == 'POST':
        subasta_form = SubastaForm(request.POST, request.FILES)
        imagenes_form = MultipleImagenSubastaForm(request.POST, request.FILES)
        
        if subasta_form.is_valid() and imagenes_form.is_valid():
            # Guardar la subasta
            subasta = subasta_form.save(commit=False)
            subasta.usuario = request.user
            subasta.precio_actual = subasta.precio_inicial
            subasta.save()
            
            # Guardar imágenes adicionales
            for imagen in request.FILES.getlist('imagenes'):
                ImagenSubasta.objects.create(
                    subasta=subasta,
                    imagen=imagen
                )
            
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
    """
    Vista para listar las subastas del usuario actual
    """
    subastas = Subasta.objects.filter(
        usuario=request.user
    ).order_by('-fecha_creacion')
    
    return render(request, 'tienda/subastas/mis_subastas.html', {
        'subastas': subastas
    })

@login_required
def finalizar_subasta(request, slug):
    """
    Vista para finalizar una subasta manualmente
    """
    subasta = get_object_or_404(Subasta, slug=slug, usuario=request.user)
    
    if subasta.estado == 'ACTIVA':
        subasta.estado = 'FINALIZADA'
        
        # Asignar ganador si hay pujas
        ultima_puja = subasta.pujas.order_by('-monto').first()
        if ultima_puja:
            subasta.ganador = ultima_puja.usuario
        
        subasta.save()
        messages.success(request, 'Subasta finalizada correctamente')
    else:
        messages.warning(request, 'La subasta ya estaba finalizada')
    
    return redirect('detalle_subasta', slug=subasta.slug)