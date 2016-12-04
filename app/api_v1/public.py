from flask_restful import Resource
from app.models import User, Note


class Statistics(Resource):
    def get(self):
        stats = {}
        stats['users'] = User.query.count()
        stats['notes'] = Note.query.count()
        return stats
