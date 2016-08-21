from datetime import datetime
from flask import render_template, redirect, \
    url_for, flash, abort, current_app, request, jsonify
from flask_login import current_user, login_required

from . import main
from .. import db
from .forms import NoteForm, ShareForm, \
    NotebookForm, SearchForm
from ..email import send_email
from ..models import User, Note, Tag, Notebook


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(
            author_id=current_user.id,
            is_deleted=False, is_archived=False).order_by(
            Note.is_favorite.desc(),
            Note.updated_date.desc()).all()
        return render_template('app/app.html', notes=notes)
    else:
        stats = {}
        users = User.query.count()
        stats['users'] = users
        notes = Note.query.count()
        stats['notes'] = notes
        return render_template('index.html', stats=stats)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.args.get('notebook'):
        notebook = Notebook.query.filter_by(
            id=int(request.args.get('notebook'))).first()
        form = NoteForm(notebook=notebook.id)
    else:
        form = NoteForm()
    form.notebook.choices = [
        (n.id, n.title) for n in
        Notebook.query.filter_by(
            author_id=current_user.id).all()]
    if form.validate_on_submit():
        print(form.body.data)
        note = Note(
            title=form.title.data,
            body=form.body.data,
            notebook_id=form.notebook.data,
            author=current_user._get_current_object())
        db.session.add(note)
        db.session.commit()

        tags = []
        if not len(form.tags.data) == 0:
            for tag in form.tags.data.split(','):
                tags.append(tag.replace(" ", ""))
            note.str_tags = (tags)
            db.session.commit()
        return redirect(url_for('main.notebook', id=note.notebook_id))
    return render_template('app/add.html', form=form)


@main.route('/settings')
@login_required
def settings():
    return render_template('app/settings.html')


@main.route('/trash')
@login_required
def trash():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(
            author_id=current_user.id,
            is_deleted=True).order_by(
                Note.updated_date.desc()).all()
        if len(notes) == 0:
            flash("Trash is empty, you are so Tidy!")
            return redirect(url_for('.index'))
        return render_template('app/trash.html', notes=notes)
    else:
        return render_template('index.html')


@main.route('/empty-trash')
@login_required
def empty_trash():
    notes = Note.query.filter_by(
        author_id=current_user.id,
        is_deleted=True).all()
    for note in notes:
        delete_forever(note.id)
    flash("Took out the Trash")
    return redirect(url_for('.index'))


@main.route('/note/<int:id>')
@login_required
def note(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    return render_template('app/note.html', notes=[note])


@main.route('/edit/<int:id>', methods=['PUT'])
@login_required
def edit(id):
    if request.is_json:
        note = Note.query.get_or_404(id)
        if current_user != note.author:
            return forbidden('Access Denied')
        note.body = request.json.get('body', note.body)
        note.body_html = request.json.get('body_html', note.body_html)
        note.updated_date = datetime.utcnow()
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_json())


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        note.is_deleted = True
        note.updated_date = datetime.utcnow()
        db.session.commit()
        flash('The note has been deleted.')
        return redirect(request.referrer)


@main.route('/delete-forever/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_forever(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        db.session.delete(note)
        db.session.commit()
        flash('So Long! The note has been deleted forever.')
        return redirect(request.referrer)


@main.route('/restore/<int:id>', methods=['GET', 'POST'])
@login_required
def restore(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        note.is_deleted = False
        note.updated_date = datetime.utcnow()
        db.session.commit()
        flash('The note has been restored.')
        return redirect(request.referrer)


@main.route('/share/<int:id>', methods=['GET', 'POST'])
@login_required
def share(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    form = ShareForm()
    if form.validate_on_submit():
        send_email(
            form.recipient_email.data, '{0} has shared \
            a braindump with you!'
            .format(current_user.email),
            'app_email/share_note',
            user=current_user, note=note)
        flash('The note has been shared!')
        return redirect(url_for('.index'))
    return render_template('app/share_note.html', form=form, notes=[note])


@main.route('/tag/<name>')
@login_required
def tag(name):
    tag = Tag.query.filter_by(tag=name).first()
    return render_template('app/tag.html', notes=tag._get_notes(), tag=name)


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


@main.route('/favorites', methods=['GET'])
@login_required
def favorites():
    heading = "Favorite Notes"
    notes = Note.query.filter_by(
        author_id=current_user.id,
        is_deleted=False,
        is_favorite=True, is_archived=False).order_by(
        Note.updated_date.desc()).all()
    if len(notes) == 0:
        flash("No favorites yet, click on the star in a note to mark \
            it as a favorite.")
        return redirect(url_for('.index'))
    return render_template('app/app.html', notes=notes, heading=heading)


@main.route('/notebook/<int:id>')
@login_required
def notebook(id):
    notebook = Notebook.query.filter_by(id=id).first()
    if current_user != notebook.author:
        abort(403)
    return render_template(
        'app/notebook.html',
        notebook=notebook,
        notes=notebook._show_notes())


@main.route('/notebook/<int:id>', methods=['DELETE'])
@login_required
def delete_notebook(id):
    notebook = Notebook.query.filter_by(id=id).first()
    if current_user != notebook.author:
        abort(403)
    else:
        notebook.is_deleted = True
        notebook.updated_date = datetime.utcnow()
        db.session.commit()
        return jsonify(notebook.to_json())

@main.route('/search')
@login_required
def search():
    form = SearchForm()
    if request.args.get('search_field', ''):
        query = request.args.get('search_field', '')
        results = Note.query.search(query) \
            .filter_by(author_id=current_user.id) \
            .order_by(Note.updated_date.desc()).all()
        if len(results) == 0:
            flash('Hmm, we did not find any \
            braindumps matching your search. Try again?')
        return render_template(
            'app/search.html',
            form=form,
            notes=results)
    return render_template(
        'app/search.html',
        form=form)


@main.route('/favorite/<int:id>', methods=['GET', 'POST'])
@login_required
def favorite(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        if not note.is_favorite:
            note.is_favorite = True
            note.updated_date = datetime.utcnow()
            db.session.commit()
            flash('Note marked as favorite')
        else:
            note.is_favorite = False
            note.updated_date = datetime.utcnow()
            db.session.commit()
            flash('Note removed as favorite')
        return redirect(request.referrer)


@main.route('/archive')
@login_required
def view_archive():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(
            author_id=current_user.id,
            is_deleted=False, is_archived=True).order_by(
                Note.updated_date.desc()).all()
        if len(notes) == 0:
            flash("Archive is empty")
            return redirect(url_for('.index'))
        return render_template('app/archive.html', notes=notes)
    else:
        return render_template('index.html')


@main.route('/archive/<int:id>')
@login_required
def archive(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        note.is_archived = True
        note.updated_date = datetime.utcnow()
        db.session.commit()
        flash('The note has been archived.')
        return redirect(request.referrer)


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
