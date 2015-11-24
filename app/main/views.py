from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask.ext.login import current_user, login_required

from . import main
from .. import db
from .forms import NoteForm
from ..models import User, Note

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():
        form = NoteForm()
        if form.validate_on_submit():
            note = Note(title=form.title.data,body=form.body.data,
                author=current_user._get_current_object())
            db.session.add(note)
            return redirect(url_for('.index'))
        notes = Note.query.filter_by(author_id=current_user.id,is_deleted=False).order_by(Note.timestamp.desc()).all()
        return render_template('index.html', form=form, notes=notes)
    else:
        return render_template('index.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        db.session.add(note)
        flash('The note has been updated.')
        return redirect(url_for('.index'))
    form.title.data = note.title
    form.body.data = note.body
    return render_template('edit_note.html', form = form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        note.is_deleted = True 
        flash('The note has been deleted.')
        return redirect(url_for('.index'))
