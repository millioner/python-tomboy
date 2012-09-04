### -*- coding: utf-8 -*- ###
"""
This code is not used yet. But it will later :)
"""
#import base64
#import json
#import urllib
#import urllib2
#
#import oauth2
#
#
#class Unauthorized(Exception):
#    """The provided email address and password were incorrect."""
#
#
#def acquire_token(email_address, password, description):
#    """Aquire an OAuth access token for the given user."""
#    # Issue a new access token for the user.
#
#    request = urllib2.Request(
#        'https://login.ubuntu.com/api/1.0/authentications?' +
#        urllib.urlencode({'ws.op': 'authenticate', 'token_name': description}))
#    request.add_header('Accept', 'application/json')
#    request.add_header('Authorization', 'Basic %s' % base64.b64encode(
#        '%s:%s' % (email_address, password)))
#    try:
#        response = urllib2.urlopen(request)
#    except urllib2.HTTPError, exc:
#        if exc.code == 401: # Unauthorized
#            raise Unauthorized("Bad email address or password")
#        else:
#            raise
#    data = json.load(response)
#    consumer = oauth2.Consumer(data['consumer_key'], data['consumer_secret'])
#    token = oauth2.Token(data['token'], data['token_secret'])
#
#    # Tell Ubuntu One about the new token.
#    get_tokens_url = (
#        'https://one.ubuntu.com/oauth/sso-finished-so-get-tokens/')
#    oauth_request = oauth2.Request.from_consumer_and_token(
#        consumer, token, 'GET', get_tokens_url)
#    oauth_request.sign_request(
#        oauth2.SignatureMethod_PLAINTEXT(), consumer, token)
#    request = urllib2.Request(get_tokens_url)
#    for header, value in oauth_request.to_header().items():
#        request.add_header(header, value)
#    response = urllib2.urlopen(request)
#
#    return consumer, token