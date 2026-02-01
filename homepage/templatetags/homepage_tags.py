from django import template

register = template.Library()


@register.filter
def chunk_list(value, size):
    """Разбивает список на чанки заданного размера."""
    if not value:
        return []
    size = int(size)
    return [value[i:i + size] for i in range(0, len(value), size)]
