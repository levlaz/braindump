from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, notes, users, errors  # noqa
