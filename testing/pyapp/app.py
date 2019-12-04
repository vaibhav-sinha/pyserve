from pydev import pydev


def health(request):
    response = pydev.Response()
    response.set_body("Service is up and healthy")
    return response
