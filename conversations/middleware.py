import jwt
from jwt import PyJWKClient
from django.conf import settings
from django.http import JsonResponse

def clerk_jwt_auth_middleware(get_response):
    def middleware(request):
        if request.path.startswith('/admin/'):
            return get_response(request)
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Unauthorized"}, status=401)

        token = auth_header.split(" ")[1]
        request.user_id = None  # Default user_id to None

        decoded_token = decode_token(token)
        # print("Decoded Token:", decoded_token)  # Print decoded token for debugging
        if decoded_token is None:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        request.user_id = decoded_token.get('sub')  # Store user ID in request
        return get_response(request)

    return middleware

def decode_token(token):
    try:
        
        jwks_client = PyJWKClient(settings.CLERK_JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        return jwt.decode(token, signing_key.key, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print("Error decoding token:", str(e))
        return None
