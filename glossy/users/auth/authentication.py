import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication

from users.models import User
from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken


# Load environment variables from .env file
load_dotenv()

# Initialize Firebase credentials
cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL"),
    }
)


default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for Firebase.
    """

    def authenticate(self, request):
        """
        Authenticate the user based on the Firebase token provided in the request.
        """
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
            email = decoded_token.get("email")
            username = decoded_token.get("name") 
        except Exception:
            raise FirebaseError()
        
        
        fcm_key = request.META.get("HTTP_FCMTOKEN")

        # Get or create the user
        user, created = User.objects.get_or_create(
            firebase_key=uid,
            defaults={
                'email': email,
                'auth_type': 'google',
                'username': username,
                'fcm_key': fcm_key

            }
        )

        # Update the username if the user was not created before
        if not user.fcm_key or user.fcm_key != fcm_key:
            user.fcm_key = fcm_key
            user.save()

        if not created and not user.username:
            user.username = username
            user.save()
        return (user, None)
