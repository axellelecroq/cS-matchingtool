import os

from flask import Flask
from .constantes import CONFIG

current_path = os.path.dirname(os.path.abspath(__file__))

templates = os.path.join(current_path, "templates")
statics = os.path.join(current_path, "static")
data = os.path.join(current_path, "data")

app = Flask("cS Matching Tool", template_folder=templates, static_folder=statics)


# local imports
from .routes import *
from .utils import generic, matching

def config_app(config_name="test"):
    """ Create the application """
    app.config.from_object(CONFIG[config_name])

    return app