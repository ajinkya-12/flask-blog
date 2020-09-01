from flask import Blueprint
from ..models import Permission

#Creating blueprint for the templates
main = Blueprint('main', __name__)

from . import views, errors

@main.app_context_processor
def injecct_permission():
    return dict(Permission = Permission)