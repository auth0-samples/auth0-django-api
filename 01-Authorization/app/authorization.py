import os

from .middleware import JsonException

from jwt import PyJWKClient, decode
from dotenv import load_dotenv
from functools import wraps
from django.http import HttpRequest, JsonResponse
from typing import Any


def authorized(function):
    @wraps(function)
    def wrap(request: HttpRequest, *args, **kwargs):
        token: RequestToken = getRequestToken(request, mutateRequest=True)

        if token is None or token.isAuthorized() is False:
            raise JsonException("Unauthorized.", 401)

        return function(request, token, *args, **kwargs)

    return wrap


def can(permission):
    def decor(function):
        @wraps(function)
        def wrap(request: HttpRequest, *args, **kwargs):
            token: RequestToken = getRequestToken(request, mutateRequest=True)

            if token is None or token.isAuthorized() is False:
                raise JsonException("Unauthorized.", 401)

            if token.hasPermission(permission) is False:
                raise JsonException("Forbidden.", 403)

            return function(request, token, *args, **kwargs)

        return wrap

    return decor


class RequestToken(object):
    def __init__(self, token: str) -> None:
        self._token: str = token

        if token is not None:
            self._decoded: dict[str, Any] | None = self.__decode__(token)
        else:
            self._decoded = None

    def __decode__(self, token: str) -> dict[str, Any] | None:
        try:
            load_dotenv()
        except:
            raise JsonException("Environment variables must be configured.", 500)

        domain: str | None = os.environ.get("AUTH0_DOMAIN")
        identifier: str | None = os.environ.get("AUTH0_API_IDENTIFIER")

        if domain is None or identifier is None:
            raise JsonException(
                "AUTH0_DOMAIN or AUTH0_API_IDENTIFIER environment variables must be configured.",
                500,
            )

        issuer: str = "https://{}/".format(domain)

        signingKey: Any = (
            PyJWKClient(issuer + ".well-known/jwks.json")
            .get_signing_key_from_jwt(self._token)
            .key
        )

        if signingKey is None:
            raise JsonException(
                "Could not retrieve a matching public key for the provided token.", 400
            )

        try:
            return decode(
                jwt=self._token,
                key=signingKey,
                algorithms=["RS256"],
                audience=identifier,
                issuer=issuer,
            )
        except:
            raise JsonException("Could not decode the provided token.", 400)

    def __str__(self) -> str:
        return self._token

    def __getattr__(self, name: str) -> Any:
        return self._decoded[name]

    def hasPermission(self, permission: str) -> bool:
        return permission in self._decoded["permissions"]

    def clear(self) -> None:
        self._decoded = None

    def isAuthorized(self) -> bool:
        return self._decoded is not None

    def dict(self) -> dict[str, Any]:
        return self._decoded if self._decoded is not None else {}


def getRequestToken(
    request: HttpRequest, mutateRequest: bool = False
) -> RequestToken | None:
    bearerToken: str | None = request.headers.get("Authorization")

    if bearerToken is None or not bearerToken.startswith("Bearer "):
        return None

    bearerToken = bearerToken.partition(" ")[2]

    if (
        request.META.get("token") is not None
        and request.META.get("bearerToken") == bearerToken
    ):
        return request.META.get("token")

    token: RequestToken = RequestToken(bearerToken)

    if mutateRequest:
        request.META["token"] = token
        request.META["bearerToken"] = bearerToken

    return token
