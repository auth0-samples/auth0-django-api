import jwt
from functools import wraps

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(request, *args, **kwargs):
            decoded = jwt.decode(request.auth, options={'verify_signature': False})
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                if required_scope in token_scopes:
                    return f(request, *args, **kwargs)
            return Response({'message': 'You don\'t have access to this resource'}, 403)
        return decorated
    return require_scope


@api_view(['GET'])
@permission_classes([AllowAny])
def public(request):
    return Response({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


@api_view(['GET'])
def private(request):
    return Response({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})


@api_view(['GET'])
@requires_scope('read:messages')
def private_scoped(request):
    return Response({'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.'})
