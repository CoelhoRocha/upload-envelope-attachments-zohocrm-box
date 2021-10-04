import os

import boxsdk
import requests
import json

from boxsdk import OAuth2, Client


def boxAuth():
    # Box Authentication
    client_id = os.getenv('client_id', 'Token Not found')
    client_secret = os.getenv('client_secret', 'Token Not found')
    url = "https://api.box.com/oauth2/token"

    payload = f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&box_subject_type=enterprise&box_subject_id=1760289'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    access_token = json_response['access_token']

    auth: OAuth2 = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
    )
    client: boxsdk.Client = Client(auth)
    return client