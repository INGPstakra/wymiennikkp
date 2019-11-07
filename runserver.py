"""
This script runs the KPSSw0.1 application using a development server.
"""

from os import environ
from KPSSw0 import app
import requests

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

    #brak url uzupełnić
