from django import template

register = template.Library()

# Ejemplo de filtro básico (puedes añadir los tuyos)
@register.filter
def formato_moneda(value):
    return f"${value:,.2f}"