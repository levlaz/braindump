from flask import g
from flask_restful import reqparse
from app import db
from app.models import User as NewUser
from app.api_v1.base import ProtectedBase


class User(ProtectedBase):
    """Work with individual notebooks."""

    parser = reqparse.RequestParser()

    # def get(self, notebook_id):
    #     """Get single notebook.

    #     Args:
    #         notebook_id (int, required): The id of the Notebook

    #     Returns:
    #         JSON representation of the notebook
    #     """
    #     return {'notebook': self.get_notebook(notebook_id).to_json()}

    def put(self):
        """Update single user.
        """
        self.parser.add_argument(
            'default_notebook', type=int,
            help="ID of the Default Notebook")
        args = self.parser.parse_args()
        user = g.user

        for arg in args:
            if args[str(arg)] is not None:
                setattr(user, arg, args[str(arg)])

        db.session.add(user)
        db.session.commit()
        return {'notebook': notebook.to_json()}

    # def delete(self, notebook_id):
    #     """Delete single notebook.

    #     Args:
    #         notebook_id (int, required): The id of the Notebook

    #     Returns:
    #         "deleted" if succeesful
    #     """
    #     db.session.delete(self.get_notebook(notebook_id))
    #     db.session.commit()
    #     return {'notebook': 'deleted'}
