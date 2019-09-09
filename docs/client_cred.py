# Configuration for OAuth2 Client Credentials Grant
# https://github.com/requests/requests-oauthlib/blob/master/docs/oauth2_workflow.rst#id12

# Allow authentication over HTTP
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import json

# farmOS Credentials
client_id = 'farmos_api_client'
client_secret = 'client_secret'
scope = 'farmos_restws_access'
token_url = 'http://localhost/oauth2/token'

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
farmOS = OAuth2Session(client=BackendApplicationClient(client_id=client_id))

# Fetch Token
farmOS.fetch_token(token_url=token_url, client_secret=client_secret)

# Fetch a protected resource
r = farmOS.get('http://localhost/node/1.json')
print(r.status_code, r.content)