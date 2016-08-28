from flask_restful import Api
from .notebooks import Notebook, NotebookList

api = Api(prefix="/api/v1", catch_all_404s=True)
api.add_resource(NotebookList, '/notebooks')
api.add_resource(Notebook, '/notebooks/<notebook_id>')
