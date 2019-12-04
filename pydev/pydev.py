import importlib
import os

ENVIRONMENT_VARIABLE = 'PYDEV_SETTINGS_MODULE'


class WSGIHandler:

    def __init__(self):
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            raise Exception('PYDEV_SETTINGS_MODULE environment setting not set')

        mod = importlib.import_module(settings_module)
        self.url_mapping = mod.URL_CONF

    def __call__(self, *args, **kwargs):
        env = args[0]
        start_response = args[1]

        request = Request(env)
        handler = self.url_mapping.get(request.path, None)
        if not handler:
            start_response('404 Not Found', [])
            return [str.encode(f'No mapping found for url {request.path}')]
        else:
            response = handler(request)
            start_response(response.status, response.headers)
            return [str.encode(response.body)]


class Request:

    def __init__(self, env):
        self.path = env['PATH_INFO']
        self.method = env['REQUEST_METHOD']


class Response:

    def __init__(self):
        self.status = '200 OK'
        self.headers = [('X-BACKEND-FRAMEWORK', 'PYDEV-1.0.0')]
        self.body = ''

    def add_header(self, name, value):
        self.headers.append((name, value))

    def set_body(self, body):
        if body:
            self.body = body


def get_wsgi_application():
    return WSGIHandler()
