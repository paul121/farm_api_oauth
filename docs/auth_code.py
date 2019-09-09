# Configuration for OAuth2 Password Credentials Grant
# https://github.com/requests/requests-oauthlib/blob/master/docs/oauth2_workflow.rst#id9

# Allow authentication over HTTP
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import json

# farmOS Credentials
client_id = 'farmos_api_client'
client_secret = 'client_secret'
scope = 'farmos_restws_access'
redirect_uri = 'http://localhost/authorized'
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


from requests_oauthlib import OAuth2Session
farmOS = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri,
                       auto_refresh_url=token_url, auto_refresh_kwargs=extra, token_updater=token_saver)

# Redirect user to farmOS for verification
authorization_url, state = farmOS.authorization_url(authorization_base_url,
                                                    access_type="offline", prompt="select_account");
print('Please go here and authorize,', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')

# Fetch the access token
farmOS.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

# Fetch a protected resource
r = farmOS.get('http://localhost/node/1.json')
all = farmOS.get('http://localhost/node.json')
all = json.loads(all.content)
print(r.status_code, r.content)