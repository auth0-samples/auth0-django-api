from authlib.integrations.django_oauth2 import ResourceProtector
from django.http import JsonResponse
from . import validator
from django.conf import settings

require_oauth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(settings.AUTH0_DOMAIN, settings.API_IDENTIFIER)
require_oauth.register_token_validator(validator)


def public(request):
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return JsonResponse(dict(message=response))


@require_oauth(None)
def private(request):
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return JsonResponse(dict(message=response))


@require_oauth("read:messages")
def private_scoped(request):
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
    return JsonResponse(dict(message=response))
