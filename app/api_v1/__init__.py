from flask_restful import Api
from .notebooks import Notebook, NotebookList
from .authentication import Token
from .user import User
from .public import Statistics

api = Api(prefix="/api/v1", catch_all_404s=True)
api.add_resource(Token, '/token', endpoint="api.token")

api.add_resource(User, '/user', endpoint="api.user")

api.add_resource(NotebookList, '/notebooks', endpoint="api.notebooks")
api.add_resource(Notebook, '/notebook/<notebook_id>', endpoint="api.notebook")

api.add_resource(Statistics, '/public/stats', endpoint="api.public")
