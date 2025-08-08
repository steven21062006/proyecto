from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.text import slugify
from django.apps import apps

@receiver(post_migrate)
def crear_categorias_predeterminadas(sender, **kwargs):
    Categoria = apps.get_model('tienda', 'Categoria')  # evita el import circular

    categorias = [
        'Vehículos Deportivos',
        'Motocicletas Urbanas',
        'Camionetas y SUV',
        'Movilidad Ecológica'
    ]
    
    for nombre in categorias:
        Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={
                'slug': slugify(nombre),
                'descripcion': f'Categoría de {nombre}'
            }
        )
