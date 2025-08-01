from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subasta, Puja, ComentarioSubasta, ImagenSubasta, Categoria
from django.forms.widgets import ClearableFileInput

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})



class SubastaForm(forms.ModelForm):
    imagen_principal = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Subasta
        fields = ['titulo', 'descripcion', 'categoria', 'imagen_principal', 'precio_inicial', 'fecha_finalizacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'fecha_finalizacion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def clean_fecha_finalizacion(self):
        fecha_fin = self.cleaned_data['fecha_finalizacion']
        if fecha_fin <= timezone.now():
            raise forms.ValidationError("La fecha de finalización debe ser en el futuro")
        return fecha_fin

class MultipleImagenSubastaForm(forms.Form):
    imagenes = forms.FileField(
        widget=ClearableFileInput(attrs={
            'class': 'form-control',
            
        }),
        label='Subir imágenes adicionales',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class ImagenSubastaForm(forms.ModelForm):
    class Meta:
        model = ImagenSubasta
        fields = ['imagen', 'orden']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }
class PujaForm(forms.ModelForm):
    class Meta:
        model = Puja
        fields = ['monto']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.subasta = kwargs.pop('subasta', None)
        super().__init__(*args, **kwargs)
        if self.subasta:
            self.fields['monto'].validators.append(
                MinValueValidator(self.subasta.precio_actual + 0.01)
            )
            self.fields['monto'].widget.attrs['min'] = float(self.subasta.precio_actual) + 0.01
    
    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if self.subasta and monto <= self.subasta.precio_actual:
            raise forms.ValidationError(
                f"El monto debe ser mayor al precio actual (${self.subasta.precio_actual:.2f})"
            )
        return monto

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioSubasta
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu pregunta o comentario...'
            })
        }

class BusquedaForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar subastas...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    precio_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo',
            'step': '0.01'
        })
    )
    precio_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo',
            'step': '0.01'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        precio_min = cleaned_data.get('precio_min')
        precio_max = cleaned_data.get('precio_max')
        
        if precio_min and precio_max and precio_min > precio_max:
            raise forms.ValidationError("El precio mínimo no puede ser mayor al precio máximo")
        
        return cleaned_data