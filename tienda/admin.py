from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Categoria, Producto, Subasta, Puja, ComentarioMoto, ComentarioSubasta

# Configuración del usuario
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Configuración de categorías
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

# Configuración de productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'disponible', 'destacado')
    search_fields = ('nombre', 'categoria__nombre')
    # Mostrar todas las categorías disponibles al crear o editar productos
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'categoria':
            kwargs["queryset"] = Categoria.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Configuración de subastas
@admin.register(Subasta)
class SubastaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'producto', 'usuario', 'precio_inicial', 'precio_actual', 'fecha_finalizacion', 'estado', 'ganador')
    list_filter = ('estado', 'fecha_finalizacion')
    search_fields = ('titulo', 'producto__nombre', 'usuario__username')
    prepopulated_fields = {"slug": ("titulo",)}
    autocomplete_fields = ['producto', 'usuario', 'ganador']

# Otros modelos
admin.site.register(Puja)
admin.site.register(ComentarioMoto)
admin.site.register(ComentarioSubasta)

