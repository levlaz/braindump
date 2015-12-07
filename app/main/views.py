from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort, current_app, request
from flask.ext.login import current_user, login_required

from . import main
from .. import db
from .forms import *
from ..email import send_email
from ..models import User, Note, Tag, Notebook

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():
        form = NoteForm()
        if form.validate_on_submit():
            note = Note(title=form.title.data,body=form.body.data, body_html=form.body_html.data, author=current_user._get_current_object())
            db.session.add(note)
            tags = []
            for tag in form.tags.data.split(','):
                tags.append(tag)
            note.str_tags = (tags)
            db.session.commit()
            return redirect(url_for('.index'))
        notes = Note.query.filter_by(author_id=current_user.id,is_deleted=False).order_by(Note.timestamp.desc()).all()
        return render_template('app/app.html', form=form, notes=notes)
    else:
        stats = []
        users = User.query.count()
        stats.append(users)
        notes = Note.query.count()
        stats.append(notes)
        return render_template('index.html', stats=stats)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = NoteForm()
    form.notebook.choices = [(n.id, n.title) for n in Notebook.query.filter_by(author_id=current_user.id).all()]
    if form.validate_on_submit():
        note = Note(title=form.title.data,body=form.body.data, body_html=form.body_html.data,notebook_id=form.notebook.data, author=current_user._get_current_object())
        db.session.add(note)
        tags = []
        for tag in form.tags.data.split(','):
            tags.append(tag.replace(" ",""))
        note.str_tags = (tags)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('app/add.html', form = form)

@main.route('/news')
def home():
    return render_template('app/news.html')

@main.route('/settings')
@login_required
def settings():
    return render_template('app/settings.html')

@main.route('/trash', methods=['GET', 'POST'])
@login_required
def trash():
    if current_user.is_authenticated():
        notes = Note.query.filter_by(author_id=current_user.id,is_deleted=True).order_by(Note.timestamp.desc()).all()
        if len(notes) == 0:
            flash("Trash is empty, you are so Tidy!")
            return redirect(url_for('.index'))
        return render_template('app/trash.html', notes=notes)
    else:
        return render_template('index.html')

@main.route('/note/<int:id>')
@login_required
def note(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    return render_template('app/note.html', notes=[note])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    form = NoteForm(notebook=note.notebook_id)
    form.notebook.choices = [(n.id, n.title) for n in Notebook.query.filter_by(author_id=current_user.id).all()]
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        note.body_html = form.body_html.data
        note.notebook_id = form.notebook.data
        db.session.add(note)
        print form.tags.data
        tags = []
        for tag in form.tags.data.split(','):
            tags.append(tag.replace(" ",""))
            print form.tags.data
            print tags
        print tags
        note.str_tags = (tags)

        db.session.commit()
        flash('The note has been updated.')
        return redirect(url_for('.index'))
    form.title.data = note.title
    form.body.data = note.body
    form.tags.data = ', '.join(note._get_tags())
    return render_template('app/edit_note.html', note=note, form = form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        note.is_deleted = True
        db.session.commit()
        flash('The note has been deleted.')
        return redirect(url_for('.index'))

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
        return redirect(url_for('.trash'))

@main.route('/restore/<int:id>', methods=['GET', 'POST'])
@login_required
def restore(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    else:
        note.is_deleted = False
        db.session.commit()
        flash('The note has been restored.')
        return redirect(url_for('.trash'))

@main.route('/share/<int:id>', methods=['GET', 'POST'])
@login_required
def share(id):
    note = Note.query.get_or_404(id)
    if current_user != note.author:
        abort(403)
    form = ShareForm()
    if form.validate_on_submit():
        send_email(form.recipient_email.data, '{0} has shared a braindump with you!'.format(current_user.username), 'app_email/share_note', user=current_user, note=note)
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
        notebook = Notebook(title=form.title.data,author_id=current_user.id)
        db.session.add(notebook)
        db.session.commit()
        return redirect(url_for('.notebooks'))

    notebooks = Notebook.query.filter_by(author_id=current_user.id, is_deleted=False).all()
    return render_template('app/notebooks.html', notebooks=notebooks, form=form)

@main.route('/notebook/<int:id>')
@login_required
def notebook(id):
    notebook = Notebook.query.filter_by(id=id).first()
    if current_user != notebook.author:
        abort(403)
    return render_template('app/notebook.html', notebook=notebook, notes=notebook._show_notes())

@main.route('/search')
@login_required
def search():
    form = SearchForm()
    if request.args.get('search_field', ''):
        query = request.args.get('search_field', '')
        results = Note.query.search(query).all()
        if len(results) == 0:
            flash('Hmm, we did not find any braindumps matching your search. Try again?')
        return render_template('app/search.html', form=form, notes=results)
    return render_template('app/search.html', form=form)


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
