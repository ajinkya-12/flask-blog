from flask import Blueprint

#Creating blueprint for the templates
main = Blueprint('main', __name__)

from . import views, errors