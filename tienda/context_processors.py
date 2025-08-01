def categorias_globales(request):
    """
    Procesador de contexto para las categorías globales.
    Modifica esto según tus necesidades reales.
    """
    from .models import Categoria  # Asegúrate de importar tu modelo Categoria
    
    categorias = Categoria.objects.all()  # Ejemplo básico
    return {
        'categorias_globales': categorias
    }