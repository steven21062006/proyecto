from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import views, auth, productos, pujas, subastas

app_name = 'tienda'

urlpatterns = [
    # Vistas principales
    path('', views.inicio, name='inicio'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('contacto/', views.contacto, name='contacto'),

    # Autenticación
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('registro/', auth.register_view, name='registro'),
    path('perfil/', auth.perfil_view, name='perfil'),  # Vista de perfil del usuario

    # Productos
    path('productos/', productos.lista_productos, name='lista_productos'),
    path('productos/<slug:categoria_slug>/', productos.lista_productos, name='productos_por_categoria'),
    path('producto/<int:id>/<slug:slug>/', productos.detalle_producto, name='detalle_producto'),

    # Pujas
    path('mis-pujas/', pujas.mis_pujas, name='mis_pujas'),
    path('api/pujas/<int:subasta_id>/', subastas.procesar_puja, name='procesar_puja'),

    # Subastas
    path('subastas/', subastas.lista_subastas, name='lista_subastas'),
    path('subastas/nueva/', subastas.crear_subasta, name='crear_subasta'),
    path('subastas/<slug:slug>/', subastas.detalle_subasta, name='detalle_subasta'),
    path('subastas/<slug:slug>/finalizar/', subastas.finalizar_subasta, name='finalizar_subasta'),
    path('subasta/<slug:slug>/comentario/', subastas.procesar_comentario_subasta, name='procesar_comentario_subasta'),
    path('mis-subastas/', subastas.mis_subastas, name='mis_subastas'),

    # Motos
    #path('motocicletas/', views.moto, name='moto'),
    path('<str:categoria>/', views.lista_categoria, name='lista_categoria'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
