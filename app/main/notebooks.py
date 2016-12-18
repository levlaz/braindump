from datetime import datetime
from flask import render_template, redirect, \
    url_for, flash, abort, current_app, request, \
    jsonify
from flask_login import current_user, login_required

from . import main
from app import db, csrf
from app.main.forms import NotebookForm
from app.models import Notebook


@main.route('/notebooks', methods=['GET', 'POST'])
@login_required
def notebooks():
    form = NotebookForm()
    if form.validate_on_submit():
        if Notebook.query.filter_by(
                title=form.title.data,
                author_id=current_user.id).first() is None:
            notebook = Notebook(
                title=form.title.data,
                author_id=current_user.id)
            db.session.add(notebook)
            db.session.commit()
        else:
            flash('A notebook with name {0} already exists.'.format(
                form.title.data))
        return redirect(url_for('.notebooks'))
    notebooks = Notebook.query.filter_by(
        author_id=current_user.id,
        is_deleted=False).all()
    return render_template(
        'app/notebooks.html',
        notebooks=notebooks,
        form=form)


@main.route('/notebook/<int:id>')
@login_required
def notebook(id):
    notebook = Notebook.query.filter_by(id=id).first()
    if current_user != notebook.author:
        abort(403)
    return render_template(
        'app/notebook.html',
        notebook=notebook,
        notes=notebook.active_notes())


@main.route('/notebook/<int:id>', methods=['DELETE'])
@login_required
def delete_notebook(id):
    notebook = Notebook.query.filter_by(id=id).first()
    if current_user != notebook.author:
        abort(403)
    else:

        if notebook.id == current_user.default_notebook:
            return jsonify({"error": "You cannot delete your default notebook!"}), 400
        else:
            notebook.is_deleted = True
            notebook.updated_date = datetime.utcnow()
            db.session.commit()

            for note in notebook.notes:
                note.is_deleted = True
                note.updated_date = datetime.utcnow()
                db.session.commit()

            return jsonify(notebook.to_json())