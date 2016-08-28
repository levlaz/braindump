from flask_restful import Resource
from flask_login import login_required


class NotebookList(Resource):
    """Show all notebooks, and add new notebook

    This is a protected resource, users must pass an
    authentication token.
    """
    method_decorators = [login_required]

    def get(self):
        """Return list of all notebooks."""
        return {'notebooks': 'all notebooks'}

    def post(self):
        """Create new notebook."""
        return {'notebook': 'new notebook'}


class Notebook(Resource):
    """Work with individual notebooks

    This is a protected resource, users must pass an
    authentication token.
    """

    def get(self, notebook_id):
        """Get single notebook."""
        return {'notebook': 'single notebook'}

    def put(self, notebook_id):
        """Update single notebook."""
        return {'notebook': 'single notebook updated'}

    def delete(self, notebook_id):
        """Delete single notebook."""
        return {'notebook': 'deleted'}
