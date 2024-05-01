from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.response import Response
from django.conf import settings


class GoogleAuth:
    def __init__(self):
        pass
    
    @staticmethod
    def auth(user_token: str):
        id_info = id_token.verify_oauth2_token(user_token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        user_id = id_info['sub']
        email_id = id_info['email']
        firstname = id_info['given_name']
        lastname = id_info["family_name"]
        return user_id,email_id,firstname,lastname
    