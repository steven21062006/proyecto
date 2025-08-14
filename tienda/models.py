from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.urls import reverse




class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subastas_por_categoria', args=[self.slug])


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)

    destacado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_producto', args=[self.id])


class Subasta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='subastas')
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subastas')
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='subastas')
    imagen_principal = models.ImageField(upload_to='subastas/')
    precio_inicial = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_finalizacion = models.DateTimeField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ACTIVA')
    ganador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subastas_ganadas')

    class Meta:
        verbose_name = 'Subasta'
        verbose_name_plural = 'Subastas'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['-fecha_inicio']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
            original_slug = self.slug
            counter = 1
            while Subasta.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        if not self.pk:
            self.precio_actual = self.precio_inicial

        if self.fecha_finalizacion < timezone.now() and self.estado == 'ACTIVA':
            self.estado = 'FINALIZADA'
            ultima_puja = self.pujas.order_by('-monto').first()
            if ultima_puja:
                self.ganador = ultima_puja.usuario

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detalle_subasta', args=[self.slug])

    @property
    def tiempo_restante(self):
        if self.estado != 'ACTIVA':
            return "Finalizada"
        delta = self.fecha_finalizacion - timezone.now()
        if delta.days < 0:
            return "Finalizada"
        return delta

    @property
    def imagen_url(self):
        if self.imagen_principal and hasattr(self.imagen_principal, 'url'):
            return self.imagen_principal.url
        return '/static/img/default_subasta.jpg'


class Puja(models.Model):
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name='pujas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pujas')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Puja'
        verbose_name_plural = 'Pujas'
        ordering = ['-fecha']
        get_latest_by = 'fecha'

    def __str__(self):
        return f"Puja de ${self.monto} en {self.subasta.titulo}"

    def save(self, *args, **kwargs):
        # Validar que la puja sea mayor que el precio actual
        if self.monto <= self.subasta.precio_actual:
            raise ValueError("El monto de la puja debe ser mayor al precio actual")
        super().save(*args, **kwargs)

        # Actualizar precio_actual de la subasta
        self.subasta.precio_actual = self.monto
        self.subasta.save()


class ComentarioSubasta(models.Model):
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['fecha']

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.subasta.titulo}"

class ComentarioMoto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}: {self.comentario[:20]}"
    

from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    pais = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=50)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    

