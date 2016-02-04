from datetime import datetime
from flask import render_template, redirect, \
    url_for, flash, abort, current_app, request, jsonify
from flask.ext.login import current_user, login_required

from . import main
from .. import db
from .forms import NoteForm, ShareForm, \
    NotebookForm, SearchForm, TaskForm
from ..email import send_email
from ..models import User, Note, Tag, Notebook, Task


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():
        notes = Note.query.filter_by(
            author_id=current_user.id,
            is_deleted=False).order_by(
            Note.is_favorite.desc(),
            Note.updated_date.desc()).all()
        return render_template('app/app.html', notes=notes)
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
        note = Note(
            title=form.title.data,
            body=form.body.data,
            body_html=form.body_html.data,
            notebook_id=form.notebook.data,
            author=current_user._get_current_object())
        db.session.add(note)
        db.session.commit()
        # adding each task list to the table
        task_list = Task.parse_markdown(note.body)
        task_ids = []
        for task_item in task_list:
            task = Task(
                title=task_item[0],
                note_id=note.id,
                notebook_id=note.notebook_id,
                author_id=current_user.id)
            db.session.add(task)
            db.session.commit()
            task_ids.append(task.id)
        # adding an id tag to the li element of each task list item
        count = 0
        body_html_list = note.body_html.split("\n")
        for i, element in enumerate(body_html_list):
            if '<li class="task-list-item">' in element:
                new_element = Task.add_id_to_li_element(
                    element, str(task_ids[count]))
                count = count + 1
                body_html_list[i] = new_element
        note.body_html = "\n".join(body_html_list)
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


@main.route('/news')
def news():
    if current_user.is_authenticated():
        return render_template('app/news.html')
    return render_template('news.html')


@main.route('/settings')
@login_required
def settings():
    return render_template('app/settings.html')


@main.route('/trash')
@login_required
def trash():
    if current_user.is_authenticated():
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
        db.session.delete(note)
        db.session.commit()
    flash("Took out the Trash")
    return redirect(url_for('.index'))


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
    form.notebook.choices = [
        (n.id, n.title) for n in
        Notebook.query.filter_by(
            author_id=current_user.id).all()]
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        note.body_html = form.body_html.data
        note.notebook_id = form.notebook.data
        note.updated_date = datetime.now()
        db.session.add(note)
        tags = []
        if not len(form.tags.data) == 0:
            for tag in form.tags.data.split(','):
                tags.append(tag.replace(" ", ""))
                print form.tags.data
                print tags
        note.str_tags = (tags)
        db.session.commit()

        # task list
        new_task_list_checked = Task.parse_markdown(note.body)
        new_task_list = [item[0] for item in new_task_list_checked]

        for item_checked in new_task_list_checked:
            item = item_checked[0]
            checked = item_checked[1]
            if item not in old_task_list:
                # need to add
                task = Task(
                    title=item,
                    is_checked=checked,
                    note_id=note.id)
                db.session.add(task)
                db.session.commit()
            else:
                # may require an update in the table
                index = old_task_list.index(item)
                old_item = old_task_list_objects[index]
                if checked != old_item.is_checked:
                    old_item.is_checked = not old_item.is_checked
                    old_item.updated_date = datetime.now()
                    if checked is True:
                        old_item.checked_date = datetime.now()
                    db.session.add(old_item)
                    db.session.commit()



        # adding the id tags to the html elements
        task_objs = Task.query.filter_by(note_id = note.id).all()
        task_ids = [item.id for item in task_objs]

        body_html_list = note.body_html.split("\n")
        for i, element in enumerate(body_html_list):
            if '<li class="task-list-item">' in element:
                task_id = Task.get_task_item_id(element, task_objs)
                new_element = Task.add_id_to_li_element(element, str(task_id))
                # count = count + 1
                body_html_list[i] = new_element
        note.body_html = "\n".join(body_html_list)
        db.session.add(note)
        db.session.commit()

        flash('The note has been updated.')
        return redirect(url_for('.index', active_note=note.id))
    form.title.data = note.title
    form.body.data = note.body
    form.tags.data = ', '.join(note._get_tags())
    return render_template('app/edit_note.html', note=note, form=form)


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
        send_email(
            form.recipient_email.data, '{0} has shared \
            a braindump with you!'
            .format(current_user.username),
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
        is_favorite=True).order_by(
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
            db.session.commit()
            flash('Note marked as favorite')
        else:
            note.is_favorite = False
            db.session.commit()
            flash('Note removed as favorite')
        return redirect(url_for('.index'))


@main.route('/tasks')
@login_required
def tasks():
    if request.args.get('status') == 'closed':
        tasks = [task for task in current_user.tasks if task.closed_date is
                 not None]
    if request.args.get('status') == 'open':
        tasks = [task for task in current_user.tasks if task.closed_date is
                 None]
    if request.args.get('status') == 'all':
        tasks = current_user.tasks
    return render_template('app/tasks.html', tasks=tasks)


@main.route('/tasks/close/<int:task_id>')
def close_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.author_id != current_user.id:
        abort(403)
    else:
        task.closed_date = datetime.utcnow()
        task.updated_date = datetime.utcnow()
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.tasks', status='open'))


@main.route('/tasks/reopen/<int:task_id>')
def reopen_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.author_id != current_user.id:
        abort(403)
    else:
        task.closed_date = None
        task.updated_date = datetime.utcnow()
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.tasks', status='closed'))


@main.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    form.notebook.choices = [
        (n.id, n.title) for n in
        Notebook.query.filter_by(
            author_id=current_user.id).all()]
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            notebook_id=form.notebook.data,
            author_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('.tasks', status="open"))
    return render_template('app/add_task.html', form=form)


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
