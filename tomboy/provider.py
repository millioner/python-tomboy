### -*- coding: utf-8 -*- ###
import urllib2
import oauth2
try:
    import json
except ImportError:
    import simplejson as json

from tomboy import settings

class TomboyProvider(object):
    """
    Provides an access to fetch tomboy notes for user from the server using OAuth API
    Documentation: https://live.gnome.org/Tomboy/Synchronization/REST/1.0
    And: https://one.ubuntu.com/developer/account_admin/auth/index
    """
    _api_urls = None

    def __init__(self, access_token, access_token_secret, tomboy_key=settings.TOMBOY_KEY, tomboy_secret=settings.TOMBOY_SECRET):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.tomboy_key = tomboy_key
        self.tomboy_secret = tomboy_secret

        self.consumer = oauth2.Consumer(tomboy_key, tomboy_secret)
        self.token = oauth2.Token(access_token, access_token_secret)
        self.client = oauth2.Client(self.consumer, self.token)


    def get_user_info(self, force_refresh=False):
        """
        Returns a dict like:
        {
            u'user-name': u'https://login.launchpad.net/+id/7eacByp',
            u'last-name': u'Smith',
            u'notes-ref': {
                u'href': u'https://one.ubuntu.com/notes/',
                u'api-ref': u'https://one.ubuntu.com/notes/api/1.0/op/' # an url for fetching notes list
            },
            u'current-sync-guid': u'0',
            u'first-name': u'David',
            u'latest-sync-revision': 925
        }
        """
        if not hasattr(self, '_user_info') or force_refresh:
            if not getattr(self, '_user_info_url', None):
                self.get_api_urls(True)
            resp, content = self.client.request(self._user_info_url, "GET")
            if resp['status'] != '200':
                raise ValueError('Cannot receive user info data. Response status: %s' % resp['status'])
            self._user_info = json.loads(content)
            self._notes_list_url = self._user_info['notes-ref']['api-ref']
        return self._user_info

    def get_notes_list(self, force_refresh=False, include_notes=True):
        """
        Returns a dict like:
        {
            u'notes': [
                {
                    u'note-content': u'Describe your new note here.',
                    u'open-on-startup': False,
                    u'last-metadata-change-date': u'2011-11-16T19:43:14.1964770+02:00',
                    u'tags': [u'system:template', u'system:notebook:pNotes - Sphinx search'],
                    u'title': u'pNotes - Sphinx search Notebook Template',
                    u'create-date': u'2011-11-16T19:43:14.1756480+02:00',
                    u'last-sync-revision': 700,
                    u'note-content-version': 1.0,
                    u'last-change-date': u'2011-11-16T19:43:14.1964770+02:00',
                    u'guid': u'00e398b4-0458-4bea-9295-9815cf72d5cb',
                    u'ref': {
                        u'href': u'https://one.ubuntu.com/notes/view/00e398b4-0458-4bea-9295-9815cf72d5cb',
                        u'api-ref': u'https://one.ubuntu.com/notes/api/1.0/op/00e398b4-0458-4bea-9295-9815cf72d5cb'
                    },
                    u'pinned': False
                },
                # ... all user's notes ...
            ],
            u'latest-sync-revision': 23
        }
        """
        if not hasattr(self, '_notes_list') or force_refresh:
            if not getattr(self, '_notes_list_url', None):
                self.get_user_info(True)
            if include_notes:
                resp, content = self.client.request('%s?include_notes=true' % self._notes_list_url, "GET")
            else:
                resp, content = self.client.request(self._notes_list_url, "GET")
            if resp['status'] != '200':
                raise ValueError('Cannot receive notes data. Response status: %s' % resp['status'])
            self._notes_list = json.loads(content)
        return self._notes_list

    def get_certain_note(self, url):
        """
        Url should be like http://domain/api/1.0/user/notes/123 or you can get one from notes_list dict
        """
        resp, content = self.client.request(url, "GET")
        if resp['status'] != '200':
            raise ValueError('Cannot receive note data. Response status: %s' % resp['status'])
        return json.loads(content)


    @classmethod
    def get_api_urls(cls, force_refresh=False):
        """
        Returns a dict like:
        {
            u'oauth_access_token_url': u'https://one.ubuntu.com/oauth/access/',
            u'user-ref': {
                u'href': u'https://one.ubuntu.com/notes/',
                u'api-ref': u'https://one.ubuntu.com/notes/api/1.0/user/'
            },
            u'api-version': u'1.0',
            u'oauth_request_token_url': u'https://one.ubuntu.com/oauth/request/',
            u'oauth_authorize_url': u'https://one.ubuntu.com/oauth/authorize/'
        }
        """
        if not cls._api_urls or force_refresh:
            f = urllib2.urlopen('%sapi/%s/' % (settings.TOMBOY_DOMAIN, settings.API_VERSION))
            cls._api_urls = json.loads(f.read())
            cls._user_info_url = cls._api_urls['user-ref']['api-ref']
        return cls._api_urls