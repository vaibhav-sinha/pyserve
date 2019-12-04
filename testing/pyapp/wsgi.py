import os

from pydev import pydev

os.environ.setdefault('PYDEV_SETTINGS_MODULE', 'testing.pyapp.settings')

application = pydev.get_wsgi_application()
