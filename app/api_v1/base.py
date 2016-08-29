from flask_restful import Resource, reqparse
from .authentication import multi_auth
from app import csrf


class ProtectedBase(Resource):
    """Base Protected Class for API Resources

    Defines that all API methods are expempt from CSRF, and
    requires either password or token based authentication.

    Initilizes basic request parser.
    """
    decorators = [multi_auth.login_required, csrf.exempt]
    parser = reqparse.RequestParser()
