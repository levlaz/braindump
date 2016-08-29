from flask_restful import Api
from .notebooks import Notebook, NotebookList
from .authentication import Token

api = Api(prefix="/api/v1", catch_all_404s=True)
api.add_resource(Token, '/token', endpoint="api.token")
api.add_resource(NotebookList, '/notebooks', endpoint="api.notebooks")
api.add_resource(Notebook, '/notebooks/<notebook_id>')
