from django.http import HttpRequest, JsonResponse
from .authorization import RequestToken, authorized, can, getRequestToken


def public(request: HttpRequest()) -> JsonResponse:
    token: RequestToken | None = getRequestToken(request)

    return JsonResponse(
        data={
            "message": "Hello from a public endpoint! You don't need to be authenticated to see this.",
            "token": token.dict() if token is not None else None,
        }
    )


@authorized
def private(request: HttpRequest, token: RequestToken) -> JsonResponse:
    return JsonResponse(
        data={
            "message": "Hello from a private endpoint! You need to be authenticated to see this.",
            "token": token.dict(),
        }
    )


@can("read:messages")
def privateScoped(request: HttpRequest, token: RequestToken) -> JsonResponse:
    return JsonResponse(
        data={
            "message": "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.",
            "token": token.dict(),
        }
    )
