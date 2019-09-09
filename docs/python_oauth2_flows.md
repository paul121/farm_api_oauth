# Using farmOS OAuth2 Flows in Python

Authorizing against the farmOS OAuth2 server is easy with the [requests-oauthlib]
library. This page documents the different OAuth2 Flows supported in farmOS. It is an adaptation of the
[requests-oauthlib library documentation] on supported OAuth2 Flows. Note that all four of the core OAuth2 Grant Types
are supported by farmOS, although the Client Credentials grant is not yet properly configured with Drupal Permissions
to access resources on the farmOS server. With the upgrade to Drupal 8, farmOS should fully support this grant type.

## Authorization Code Grant

The Authorization Code grant type is probably the most common 3rd party grant type used for OAuth2 Authorization.
This flow is great for 3rd party applications because it does not require them to store the resource user's credentials -
instead, the 3rd party application redirects the user to login to farmOS and authorize access for the application.

The process is as follows:
 1. You must know the `client_id`, `client_secret` and `redirect_uri` for the farmOS API client. These values can be
 saved in Python.
 2. Authorize the user through redirection. An `authroization_url` is created for the user to login.
 3. Successful login and authorization creates an `authorization_code` embedded in the redirect URL. This code is used
 for the client to `fetch()` an `access_token` and `refresh_token`.
 4. With a valid `access_token`, requests can be made to protected resources on the farmOS server. The `access_token` is authenticated
 as the farmOS user account used to authorize and create the `access_token`. Only resources available to the user will be
 available to the `access_token`.
 5. By default the `access_token` will expire after 3600 seconds (1 hour). After this, the `refresh_token` is used to
 generate a new `access_token`. The code below shows how the [requests-oauthlib] handles token expiration and token
 regeneration automatically with a `token_saver` utility.
 

```python
# Configuration for OAuth2 Authorization Code Grant
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
```

## Implicit Grant Type

The Implicit grant type is used for 3rd party OAuth2 Authorization where the `client_secret` or user `password` should
not be stored. A common example is with JavaScript Single Page Applications.

Similar to the Authorization Code grant, the Implicit grant requires users to login to farmOS and authorize the 3rd
party application access to the requested scopes. The difference is that an `authorization_code` is not returned but
rather an `access_token`. The downside is that there is no `refresh_token` provided with this grant type.

The process is as follows:
 1. You must know the `client_id` and `redirect_uri` for the farmOS API client. These values can be
 saved in Python.
 2. Authorize the user through redirection. An `authroization_url` is created for the user to login.
 3. Successful login and authorization redirects the user to the `redirect_uri` with the `access_token` embedded
 in the URL.
 4. Parse the `access_token` from the `redirect_response` url.
 5. By default the `access_token` will expire after 3600 seconds (1 hour). There is no `refresh_token` provided to
 generate a new `access_token` after expiration.
 
```python
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
```

## Password Credentials Grant
```python
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
```

## Client Credentials Grant
```python
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
```


[requests-oauthlib]: https://github.com/requests/requests-oauthlib
[requests-oauthlib library documentation]: https://github.com/requests/requests-oauthlib/blob/master/docs/oauth2_workflow.rst