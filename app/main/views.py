from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask.ext.login import current_user

from . import main
from .. import db
from .forms import NoteForm
from ..models import User, Note

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data,body=form.body.data,
            author=current_user._get_current_object())
        db.session.add(note)
        return redirect(url_for('.index'))
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('index.html', form=form, notes=notes)
