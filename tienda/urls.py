from django.urls import path
from .views.auth import login_view
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    views,
    auth,
    productos,
    pujas,
    subastas
)

app_name = 'tienda'

urlpatterns = [
    # Vistas principales
    path('', views.inicio, name='inicio'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),

    # Autenticación
    path('login/', login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('registro/', auth.register_view, name='registro'),

    # Productos
    path('productos/', productos.lista_productos, name='lista_productos'),
    path('productos/<slug:categoria_slug>/', productos.lista_productos, name='productos_por_categoria'),
    path('producto/<int:id>/<slug:slug>/', productos.detalle_producto, name='detalle_producto'),

    # Pujas
    path('pujar/<int:producto_id>/', pujas.hacer_puja, name='hacer_puja'),
    path('mis-pujas/', pujas.mis_pujas, name='mis_pujas'),

    # Subastas
    path('subastas/', subastas.lista_subastas, name='lista_subastas'),
    path('subastas/nueva/', subastas.crear_subasta, name='crear_subasta'),
    path('subastas/<slug:slug>/', subastas.detalle_subasta, name='detalle_subasta'),
    path('subastas/<slug:slug>/finalizar/', subastas.finalizar_subasta, name='finalizar_subasta'),
    path('mis-subastas/', subastas.mis_subastas, name='mis_subastas'),

    # Auto deportivo (subasta especial)
        # Auto deportivo (subasta especial)
    path('auto-deportivo/', subastas.detalle_auto_deportivo, name='detalle_auto_deportivo'),
    path('api/pujas/auto-deportivo/', subastas.procesar_puja_auto, name='pujar_auto'),
    #apple watch
    path('apple-watch/', subastas.apple_watch, name='apple_watch'),
    path('api/pujas/apple-watch/', subastas.procesar_puja_apple, name='pujar_apple'),

    path('motocicletas/', views.moto, name='moto'),
    #yamaha
    path('yamaha-moto/', subastas.yamaha, name='yamaha'),
    path('api/pujas/yamaha-moto/', subastas.procesar_puja_yamaha, name='pujar_yamaha'),
  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
