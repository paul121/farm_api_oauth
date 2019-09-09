# Configuration for OAuth2 Implicit Grant
# https://github.com/requests/requests-oauthlib/blob/master/docs/oauth2_workflow.rst#id10

# Allow authentication over HTTP
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import json

# farmOS Credentials
client_id = 'farmos_api_client'
scope = 'farmos_restws_access'
authorization_base_url = 'http://localhost/oauth2/authorize'
token_url = 'http://localhost/oauth2/token'

from oauthlib.oauth2 import MobileApplicationClient
from requests_oauthlib import OAuth2Session
farmOS = OAuth2Session(client=MobileApplicationClient(client_id=client_id), scope=scope)

# Redirect user to farmOS for verification
authorization_url, state = farmOS.authorization_url(authorization_base_url);
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
# NOTE: This is not mentioned in the requests-oauth2lib documentation
#   but a login to farmOS and accepting the form is required.
redirect_response = input('Paste the full redirect URL here:')
response = farmOS.get(redirect_response)
farmOS.token_from_fragment(response.url)

# Fetch a protected resource
r = farmOS.get('http://localhost/node/1.json')
all = farmOS.get('http://localhost/node.json')
all = json.loads(all.content)
print(r.status_code, r.content)