from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from app.models import User
from flask_restful import Resource

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


class Token(Resource):
    """Generate Auth Token"""
    decorators = [multi_auth.login_required]

    def get(self):
        """Return JWT Token"""
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}


@basic_auth.verify_password
def verify_password(email, password):
    g.user = None
    try:
        user = User.query.filter_by(email=email).first()
        if user.verify_password(password):
            g.user = user
            return True
    except:
        return False


@token_auth.verify_token
def verify_token(token):
    try:
        g.user = User.verify_auth_token(token)
        return True
    except:
        False
