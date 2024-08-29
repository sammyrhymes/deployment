from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return ''

@register.filter
def item_count(queryset):
    return queryset.count()
