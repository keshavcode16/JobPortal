import requests
from app.settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET

FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
FACEBOOK_DEBUG_TOKEN_URL = "https://graph.facebook.com/debug_token"
FACEBOOK_AUTH_NO_EMAIL = "{}@facebook.com"


class FacebookAuth:
    def __init__(self):
        pass

    @staticmethod
    def auth(user_token: str):
        appToken = requests.get(FACEBOOK_ACCESS_TOKEN_URL, params=dict(
            client_id=FACEBOOK_APP_ID,
            client_secret=FACEBOOK_APP_SECRET,
            grant_type='client_credentials'
        )).json()['access_token']

        user_data = requests.get(FACEBOOK_DEBUG_TOKEN_URL, params=dict(
            input_token=user_token,
            access_token=appToken
        )).json()

        user_id = user_data['data']['user_id']
        email = user_data.get("data").get("email")
        return user_id, email

