import time
from threading import local


thread_locals = local()


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals.path = request.path
        thread_locals.sql_count = 0
        thread_locals.sql_total = 0
        timestamp = time.monotonic()

        response = self.get_response(request)

        data = {
            'uuid': request.META.get('HTTP_UUID'),
            'c_started': request.META.get('HTTP_C_STARTED'),
            'path': request.path,
            'request_total': round(time.monotonic() - timestamp, 3),
            'sql_count': thread_locals.sql_count,
            'sql_total': round(thread_locals.sql_total, 3),
        }

        for key, value in data.items():
            response[key.capitalize().replace("_", "-")] = value

        thread_locals.sql_total = 0
        thread_locals.sql_count = 0
        thread_locals.path = ''

        return response
