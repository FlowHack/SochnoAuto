from django import template

register = template.Library()


@register.filter
def division_price(value: int) -> str:
    """Форматирование цены (разделение по тысячам)

    Args:
        value (int): Цена

    Returns:
        str: Форматированная строка
    """

    return f'{value:,}'.replace(',', ' ')
