from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Note
from . import api
from .errors import forbidden


@api.route('/notes/', methods=['POST'])
def new_note():
    note = Note.from_json(request.json)
    note.author = g.current_user
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_json(), 201, \
            {'Location': url_for('api.get_note', id=note.id, _external=True)})

@api.route('/notes/<int:id>', methods=['PUT'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if g.current_user != note.author:
        return forbidden('Access Denied')
    note.body = request.json.get('body', note.body)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_json())

@api.route('/notes/')
def get_notes():
    notes = Note.query.filter_by(author=g.current_user).all()
    return jsonify({ 'notes': [note.to_json() for note in notes] })

@api.route('/notes/<int:id>')
def get_note(id):
    note = Note.query.get_or_404(id)
    if g.current_user != note.author:
        abort(403)
    return jsonify(note.to_json())
