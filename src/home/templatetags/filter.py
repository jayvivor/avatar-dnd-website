from django import template
from commonutils import utils

register = template.Library()

@register.filter(name="nl_listed")
def nl_listed(iterable):
    return utils.nl_listed([str(model) for model in iterable], style=" / ", use_and=False)