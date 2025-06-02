from django import template

register = template.Library()

@register.filter
def currency(value):
    try:
        value = float(value)
        return "₱{:,.2f}".format(value)
    except (ValueError, TypeError):
        return "₱0.00"
