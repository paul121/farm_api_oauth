# Configuration for OAuth2 Password Credentials Grant
# https://github.com/requests/requests-oauthlib/blob/master/docs/oauth2_workflow.rst#id11

# Allow authentication over HTTP
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import json

# farmOS Settings
client_id = 'farmos_api_client'
client_secret = 'client_secret'
username = 'paul'
password = 'test'
scope = 'farmos_restws_access'
authorization_base_url = 'http://localhost/oauth2/authorize'
token_url = 'http://localhost/oauth2/token'
extra = {
    'client_id' : client_id,
    'client_secret' : client_secret,
}

# Create a token_save to handle automatic saving and handling of refresh tokens
# https://github.com/requests/requests-oauthlib/blob/master/docs/oauth2_workflow.rst#id19
def token_saver(token):
    print("Got a new token: " + token['access_token'] + " expires in " + token['expires_in'])

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
farmOS = OAuth2Session(client=LegacyApplicationClient(client_id=client_id), scope=scope,
                       auto_refresh_url=token_url, auto_refresh_kwargs=extra, token_updater=token_saver)

farmOS.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret, username=username, password=password)

# Fetch a protected resource
r = farmOS.get('http://localhost/node/1.json')
all = farmOS.get('http://localhost/node.json')
all = json.loads(all.content)
print(r.status_code, r.content)