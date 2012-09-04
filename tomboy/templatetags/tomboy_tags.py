### -*- coding: utf-8 -*- ###
from django import template

from ..formatter import convert_note_to_html
register = template.Library()

@register.filter
def tomboy_to_html(note):
    return convert_note_to_html(note)