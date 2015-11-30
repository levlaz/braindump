from flask import jsonify
from . import api
from ..models import Note


@api.route('/notes')
#@auth.login_required
def get_notes():
    notes = Note.query.all()
    return jsonify({ 'notes': [note.to_json() for note in notes] })

@api.route('/notes/<int:id>')
#@auth.login_required
def get_note(id):
    note = Note.query.get_or_404(id)
    return jsonify(note.to_json())
