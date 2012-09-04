### -*- coding: utf-8 -*- ###
from django.template.response import TemplateResponse

from tomboy.decorators import get_tomboy_access
from tomboy.provider import TomboyProvider

def home(request, template='home.html'):
    """
    Just small home page
    """
    return TemplateResponse(request, template, {})

@get_tomboy_access() # it's highly recommended to provide here your own "get_saved_token" function (see the manual or source code)
def show_notes(request, tomboy_access_data, template='show_notes.html'):
    """
    tomboy_access_data is provided by "get_tomboy_access" decorator
    it is a dict like:
    {
        'success': True,
        'error': None,
        'access_token': 'sadk.agsldfja;sdfaoekarerkaweo;rfaweiu5welrjkwer',
        'access_token_secret': 'sdfklajsldifjaiejrqwl3rp23fpqNEFAWRKFHSDKG'
    }
    """
    if tomboy_access_data['success']:
        # it's VERY good idea to save tomboy_access_data['access_token'] and tomboy_access_data['access_token_secret'] here
        provider = TomboyProvider(tomboy_access_data['access_token'], tomboy_access_data['access_token_secret'])
        user_data = provider.get_user_info()
        notes = provider.get_notes_list()
        return TemplateResponse(request, template, { 'notes': notes.get('notes', []), 'user_data': user_data })
    else:
        from django.http import HttpResponseServerError
        return HttpResponseServerError(tomboy_access_data['error'])