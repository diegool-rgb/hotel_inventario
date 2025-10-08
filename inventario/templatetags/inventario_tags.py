from django import template
from django.http import QueryDict

register = template.Library()

@register.simple_tag(takes_context=True)
def url_with_params(context, **kwargs):
    """
    Genera una URL manteniendo los parámetros actuales y agregando/modificando los especificados
    """
    request = context['request']
    query_dict = request.GET.copy()
    
    for key, value in kwargs.items():
        if value:
            query_dict[key] = value
        elif key in query_dict:
            del query_dict[key]
    
    return '?' + query_dict.urlencode() if query_dict else ''

@register.filter
def get_item(dictionary, key):
    """
    Obtiene un item de un diccionario usando una clave dinámica
    """
    return dictionary.get(key)

@register.filter
def format_currency(value):
    """
    Formatea un número como moneda chilena
    """
    try:
        return f"${int(value):,}".replace(',', '.')
    except (ValueError, TypeError):
        return value