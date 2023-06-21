import logging
from django.http import JsonResponse


class JsonException(Exception):
    pass


class JsonExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, JsonException):
            return None

        message, code = exception.args
        logging.error(exception)

        return JsonResponse(data={"error": message}, status=code)
