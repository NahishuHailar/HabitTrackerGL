from firebase_admin import auth

def get_user_cred(request):
    """
    Get user credentials (user firebase_key)
    from the Google Firebase token.
    Works only with Google Firebase auth.
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    id_token = auth_header.split(" ").pop()
    decoded_token = auth.verify_id_token(id_token)
    firebase_key = decoded_token.get("uid")
    return firebase_key
