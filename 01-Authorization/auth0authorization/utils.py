from urllib.error import URLError

import jwt

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    key_client = jwt.PyJWKClient('https://{}/.well-known/jwks.json'.format(settings.AUTH0_DOMAIN))
    try:
        public_key = key_client.get_signing_key(header['kid']).key
    except (jwt.PyJWKClientError, URLError):
        raise AuthenticationFailed('Public key not found.')

    api_identifier = settings.API_IDENTIFIER
    issuer = settings.JWT_ISSUER
    return jwt.decode(token, public_key, audience=api_identifier, issuer=issuer, algorithms=['RS256'])
