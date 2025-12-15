from django import template

register = template.Library()

@register.filter(name="endswith")
def endswith(value, arg):
    return value.lower().endswith(arg.lower())

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})