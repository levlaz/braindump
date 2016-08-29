from flask import g, jsonify
from app import csrf, db
from app.models import Notebook as NewNotebook
from app.api_v1.base import ProtectedBase


class NotebookList(ProtectedBase):
    """Show all notebooks, and add new notebook

    This is a protected resource, users must pass an
    authentication token.
    """

    def get(self):
        """Return list of all notebooks."""
        return {'notebooks': list(map(
            lambda notebook: notebook.to_json(), g.user.notebooks.all()))}

    def post(self):
        """Create new notebook."""
        self.parser.add_argument(
            'title', type=str, help='Tite of the Notebook')
        args = self.parser.parse_args()
        notebook = NewNotebook(
            title=args['title'],
            author_id=g.user.id,
        )
        db.session.add(notebook)
        db.session.commit()
        return {'notebook': notebook.to_json()}, 201


class Notebook(ProtectedBase):
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
