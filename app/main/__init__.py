from flask import Blueprint

_main = Blueprint('main', __name__)

@_main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)
	pass

from ..models import Permission


@_main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)