from .parser import CustomConfigParser
import os
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import requests
"""This module needs to access creds.ini file and use data to obtain
    access and refresh tokens. 
    Access token only valid for 1 hour.

    Whenever a command needs to make a request to Teem it will use the stored
    access token or if that has expired (request denied), obtain a new token
    using refresh.
    If no refresh token stored then obtain using credentials.

    Request (denied) -> Refresh Token (none stored) -> Obtain refresh token.

    Would it be simpler and less work to just obtain a new token with each request?
    Maybe, seems...wrong.
"""
def load_credentials():
    parser = CustomConfigParser()
    home = os.environ['HOME']
    credentials = f"{home}\\.teem\\credentials.ini"
    return parser.get_data(credentials)
    

def obtain_token(client_id, client_secret, username, password, token_url, scope):
    """Inputs: Access key, Secret key, username, password, authentication URL, scope
        Outputs: dictionary containing access token and refresh token"""
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id, scope = scope))
    token = oauth.fetch_token(token_url=token_url,
                          username=username,
                          password=password,
                          client_id=client_id,
                          client_secret=client_secret)
    resp = {}
    resp['access_token'] = token['access_token']
    resp['refresh_token'] = token['refresh_token']
    return resp

def refresh_token(client_id, client_secret, refresh_token):
    url = 'https://app.teem.com/oauth/token/'
    payload = {'client_id': client_id,
           'client_secret': client_secret,
           'grant_type': 'refresh_token',
           'refresh_token': refresh_token
           }
    r = requests.post(url, params=payload)
    r.raise_for_status()
    response = r.json()
    resp = {}
    resp['access_token'] = response['access_token']
    resp['refresh_token'] = response['refresh_token']
    return resp
 

if __name__ == '__main__':
    creds = load_credentials()
    print(creds)
    resp = obtain_token(creds['teem_access_key_id'], creds['teem_secret_access_key'],
                        creds['teem_username'], creds['teem_password'],
                        'https://app.teem.com/oauth/token/',
                        ['users', 'reservations', 'accounts'])
    print(resp)
    resp2 = refresh_token(creds['teem_access_key_id'], creds['teem_secret_access_key'],
                          resp['refresh_token'])
    print(resp2)
    
