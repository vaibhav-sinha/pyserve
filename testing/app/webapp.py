def app(env, start_response):
    start_response('200 OK', [('CUSTOM_HEADER', 'Find this is Developer Tools')])
    return [str.encode('''<html><head><h1>This is dynamic content. Trust me.</h1></head></html>''')]


application = app
