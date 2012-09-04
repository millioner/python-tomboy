### -*- coding: utf-8 -*- ###
import urllib
import urlparse

from django.http import HttpResponseRedirect

import oauth2

from tomboy import settings
from .provider import TomboyProvider

def get_saved_token_from_session(request):
    """
    Returns previously saved token from the session
    IMPORTANT: highly recommended to provide your own custom function which will retrieve token from better storage
    """
    return {
        'access_token': request.session.get('tomboy_access_token'),
        'access_token_secret': request.session.get('tomboy_access_token_secret')
    }

def get_tomboy_access(get_saved_token=get_saved_token_from_session):
    """
         Provides OAuth authorisation via tomboy server for django project
            **get_saved_token** - some function returns previously saved token like a dict.
                                  Highly recommended to provide the custom one and permanently save a token for each user.
                                  Default function retrieves token from the session which is not very good approach.

         Links: https://one.ubuntu.com/developer/account_admin/auth/index
                https://live.gnome.org/Tomboy/Synchronization/REST/1.0
         Usage:
         =======================
            from tomboy.decorators import get_tomboy_access
            from tomboy.provider import TomboyProvider

            def get_saved_token(request):
                # get saved token pair from DataBase, Profile, Cache or something
                # it's highly recommended to provide such function
                # and also save token each time in the view for each user
                # ...
                return {
                    'tomboy_access_token': 'access_token',
                    'tomboy_access_token_secret': 'secret_token'
                }

            @get_tomboy_access(get_saved_token):
            def some_view_for_getting_access_to_tomboy(request, tomboy_access_data, *args, **kwargs):
                if tomboy_access_data['success']:
                    # it's highly recommended to permanently save
                    # tomboy_access_data['access_token'] and tomboy_access_data['access_token_secret']
                    # for current user here (and return it in get_saved_token function)

                    provider = TomboyProvider(tomboy_access_data['access_token'], tomboy_access_data['access_token_secret'])
                    notes_list = provider.get_notes_list()
                    ...
                else:
                    from django.http import HttpResponseServerError
                    return HttpResponseServerError(tomboy_access_data['error'])
         =======================
    """

    def tomboy_decorator(view):

        def get_oauth_callback(request):
            res = '%s://%s%s' % (
                'https' if request.is_secure() else 'http',
                request.get_host(),
                request.get_full_path()
            )
            return urllib.quote(res)

        def wrapped_func(request, *args, **kwargs):
            result = { 'provider': None, 'success': False, 'error': None }
            saved_access_token = get_saved_token(request)
            if not saved_access_token.get('access_token') or not saved_access_token.get('access_token_secret'):
                api_urls = TomboyProvider.get_api_urls()
                consumer = oauth2.Consumer(settings.TOMBOY_KEY, settings.TOMBOY_SECRET)
                if 'tomboy_request_token' not in request.session or 'tomboy_request_token_secret' not in request.session:
                    # step #1
                    client = oauth2.Client(consumer)
                    resp, content = client.request('%s?oauth_callback=%s' % (
                        api_urls['oauth_request_token_url'],
                        get_oauth_callback(request)
                    ), "POST")
                    if resp['status'] != '200':
                        result['error'] = "Cannot receive request token: invalid response %s." % resp['status']
                    else:
                        # step #2
                        try:
                            request_token = dict(urlparse.parse_qsl(content))
                            request.session['tomboy_request_token'] = request_token['oauth_token']
                            request.session['tomboy_request_token_secret'] = request_token['oauth_token_secret']
                            return HttpResponseRedirect("%s?oauth_token=%s" % (
                                api_urls['oauth_authorize_url'],
                                request_token['oauth_token']
                            ))
                        except (KeyError, ValueError, TypeError):
                            result['error'] = "Cannot receive request token: invalid response content %s." % content
                else:
                    if 'oauth_verifier' not in request.GET:
                        result['error'] = "Cannot receive oauth_verifier. It's missing in GET params"
                    else:
                        # step #3
                        token = oauth2.Token(
                            request.session['tomboy_request_token'],
                            request.session['tomboy_request_token_secret']
                        )
                        token.set_verifier(request.GET['oauth_verifier'])
                        client = oauth2.Client(consumer, token)

                        resp, content = client.request(api_urls['oauth_access_token_url'], "POST")
                        if resp['status'] != '200':
                            result['error'] = "Cannot receive an access token: invalid response %s." % resp['status']
                        else:
                            try:
                                access_token = dict(urlparse.parse_qsl(content))
                                request.session['tomboy_access_token'] = access_token['oauth_token']
                                request.session['tomboy_access_token_secret'] = access_token['oauth_token_secret']
                                result['success'] = True
                                result['access_token'] = access_token['oauth_token']
                                result['access_token_secret'] = access_token['oauth_token_secret']
                            except (KeyError, ValueError, TypeError):
                                result['error'] = "Cannot receive request token: invalid response content %s." % content
            else:
                result['success'] = True
                result['access_token'] = request.session['tomboy_access_token']
                result['access_token_secret'] = request.session['tomboy_access_token_secret']

            return view(request, result, *args, **kwargs)

        return wrapped_func

    return tomboy_decorator