#!/usr/local/bin/python3
from wsgiref.handlers import CGIHandler
#from helloFlask import app

from views import app

#from flaskr import create_app
#app = create_app()
CGIHandler().run(app)
