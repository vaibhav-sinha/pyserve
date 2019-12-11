import sys


class DummyGateway:

    def process(self, path, input, write):
        response = f'''HTTP/1.1 200 OK
            Date: Mon, 27 Jul 2009 12:28:53 GMT
            Server: Apache/2.2.14 (Win32)
            Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
            Content-Type: text/html
            Connection: Closed

            <html>
            <body>
            <h1>Hello, World!</h1>
            <h2>{path}</h2>
            </body>
            </html>'''

        write(str.encode(response))


class WSGI:

    # https://www.python.org/dev/peps/pep-3333/

    def __init__(self, app_loc, app_module, app):
        import importlib.util
        spec = importlib.util.spec_from_file_location(app_module, app_loc + f"/{app_module}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.app = getattr(module, app)

    def process(self, path, input, write):
        env = {
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '9989',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': input,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False
        }

        headers = []

        def start_response(status, response_headers, exc_info=None):
            nonlocal headers
            headers = [status, response_headers]

        outputs = self.app(env, start_response)

        status, response_headers = headers
        write(str.encode('HTTP/1.1: %s\r\n' % status))
        for header in response_headers:
            write(str.encode('%s: %s\r\n' % header))
        write(str.encode('\r\n'))

        for output in outputs:
            write(output)
