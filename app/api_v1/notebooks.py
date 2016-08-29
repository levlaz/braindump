from flask import g
from flask_restful import reqparse
from app import db
from app.models import Notebook as NewNotebook
from app.api_v1.base import ProtectedBase


class NotebookList(ProtectedBase):
    """Show all notebooks, and add new notebook"""

    parser = reqparse.RequestParser()

    def get(self):
        """Return list of all notebooks."""
        return {'notebooks': list(map(
            lambda notebook: notebook.to_json(), g.user.notebooks.all()))}

    def post(self):
        """Create new notebook.

        Args: (Via Request Parameters)
            title (string, required): The title of the new Notebook

        Returns:
            JSON representation of the newly created notebook
        """
        self.parser.add_argument(
            'title', required=True,
            type=str, help='Missing Title of the Notebook')
        args = self.parser.parse_args()
        notebook = NewNotebook(
            title=args['title'],
            author_id=g.user.id,
        )
        db.session.add(notebook)
        db.session.commit()
        return {'notebook': notebook.to_json()}, 201


class Notebook(ProtectedBase):
    """Work with individual notebooks."""

    parser = reqparse.RequestParser()

    @staticmethod
    def get_notebook(notebook_id):
        return g.user.notebooks.filter_by(
            id=notebook_id).first_or_404()

    def get(self, notebook_id):
        """Get single notebook."""
        return {'notebook': self.get_notebook(notebook_id).to_json()}

    def put(self, notebook_id):
        """Update single notebook."""
        self.parser.add_argument(
            'title', type=str,
            help="Title of the Notebook")
        self.parser.add_argument(
            'is_deleted', type=bool, help="True if notebook is deleted")
        args = self.parser.parse_args()
        notebook = self.get_notebook(notebook_id)

        print(args)
        for arg in args:
            if args[str(arg)] is not None:
                setattr(notebook, arg, args[str(arg)])

        db.session.add(notebook)
        db.session.commit()
        return {'notebook': notebook.to_json()}

    def delete(self, notebook_id):
        """Delete single notebook."""
        db.session.delete(self.get_notebook(notebook_id))
        db.session.commit()
        return {'notebook': 'deleted'}
