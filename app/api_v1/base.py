from flask_restful import Resource
from .authentication import multi_auth
from app import csrf


class ProtectedBase(Resource):
    """Base Protected Class for API Resources

    Defines that all API methods are expempt from CSRF, and
    requires either password or token based authentication.

    Basic Authentication can be passed via the headers. A token can be obtained
    from /api/v1/token and passed as a "Bearer" in the Authentication headers.
    """
    decorators = [multi_auth.login_required, csrf.exempt]
