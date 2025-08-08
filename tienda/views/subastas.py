from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

from tienda.models import Producto, Puja, ComentarioMoto, Subasta
from tienda.forms import SubastaForm, PujaForm, MultipleImagenSubastaForm




def detalle_yamaha(request):
    producto = get_object_or_404(Producto, nombre="Yamaha R3")
    subasta = get_object_or_404(Subasta, producto=producto)

    mensaje_puja = None
    mensaje_comentario = None

    if request.method == "POST":
        if 'monto' in request.POST:
            try:
                monto = float(request.POST['monto'])
                puja_actual = Puja.objects.filter(subasta=subasta).order_by('-monto').first()
                precio_actual = puja_actual.monto if puja_actual else producto.precio

                if monto <= precio_actual:
                    mensaje_puja = "El monto debe ser mayor que la puja actual."
                else:
                    Puja.objects.create(
                        usuario=request.user,
                        subasta=subasta,
                        monto=monto,
                        fecha=timezone.now()
                    )
                    mensaje_puja = "Puja registrada correctamente!"
            except Exception:
                mensaje_puja = "Monto inválido."

        elif 'comentario' in request.POST:
            texto = request.POST.get('comentario', '').strip()
            if texto:
                ComentarioMoto.objects.create(
                    producto=producto,
                    nombre=request.user.username,
                    comentario=texto,
                    fecha=timezone.now()
                )
                mensaje_comentario = "Comentario agregado."
            else:
                mensaje_comentario = "No puedes enviar un comentario vacío."

    comentarios = ComentarioMoto.objects.filter(producto=producto).order_by('-fecha')
    pujas = Puja.objects.filter(subasta=subasta).order_by('-monto')

    context = {
        'producto': producto,
        'comentarios': comentarios,
        'pujas': pujas,
        'user': request.user,
        'mensaje_puja': mensaje_puja,
        'mensaje_comentario': mensaje_comentario,
    }
    return render(request, 'tienda/subastas/yamaha.html', context)








def procesar_comentario_yamaha(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', '').strip()
            if not texto:
                return JsonResponse({'success': False, 'message': 'El comentario no puede estar vacío'}, status=400)

            producto = Producto.objects.get(nombre="Yamaha R3")

            nuevo_comentario = ComentarioMoto.objects.create(
                producto=producto,
                usuario=request.user,
                texto=texto,
                fecha=timezone.now()
            )

            return JsonResponse({
                'success': True,
                'nuevo_comentario': {
                    'usuario': nuevo_comentario.usuario.username,
                    'texto': nuevo_comentario.texto,
                    'fecha': nuevo_comentario.fecha.strftime("%d/%m/%Y %H:%M")
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


def detalle_auto_deportivo(request):
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


def procesar_puja_auto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto'))

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


def apple_watch(request):
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


def procesar_puja_apple(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto'))

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


def detalle_subasta(request, slug):
    subasta = get_object_or_404(Subasta, slug=slug)
    puja_form = None

    if subasta.estado == 'ACTIVA' and subasta.usuario != request.user:
        if request.method == 'POST':
            puja_form = PujaForm(request.POST, subasta=subasta)
            if puja_form.is_valid():
                puja = puja_form.save(commit=False)
                puja.subasta = subasta
                puja.usuario = request.user
                puja.save()

                subasta.precio_actual = puja.monto
                subasta.save()

                messages.success(request, '¡Puja realizada con éxito!')
                return redirect('detalle_subasta', slug=subasta.slug)
        else:
            puja_form = PujaForm(subasta=subasta)

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
