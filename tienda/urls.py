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
    
    path('mis-pujas/', pujas.mis_pujas, name='mis_pujas'),

    # Subastas
    path('subastas/', subastas.lista_subastas, name='lista_subastas'),
    path('subastas/nueva/', subastas.crear_subasta, name='crear_subasta'),
    path('subastas/<slug:slug>/', subastas.detalle_subasta, name='detalle_subasta'),
    path('subastas/<slug:slug>/finalizar/', subastas.finalizar_subasta, name='finalizar_subasta'),
    path('mis-subastas/', subastas.mis_subastas, name='mis_subastas'),

    

    path('motocicletas/', views.moto, name='moto'),
    #yamaha
    
  # Añade estas dos líneas en la sección de Yamaha para comentarios y pujas vía API
    
    #path('yamaha-moto/', subastas.detalle_yamaha, name='yamaha'),
    path('subasta/<slug:slug>/comentario/', subastas.procesar_comentario_subasta, name='procesar_comentario_subasta'),
    
    path('motos/', views.lista_motos, name='lista_motos'),
    path('', views.inicio, name='inicio'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
