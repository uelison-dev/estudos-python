
from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name="reais")
def reais(valor):
    try:
        valor = Decimal(str(valor))
        formatado = f"{valor:,.2f}"
        formatado = formatado.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatado}"
    except (ValueError, TypeError, InvalidOperation):
        return "R$ 0,00"
