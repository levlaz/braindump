import hashlib

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from flask.ext.login import UserMixin, current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from app.exceptions import ValidationError
from flask.ext.sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
import re
from lxml import etree
from lxml import html

make_searchable()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
Association Table to resolve M:M Relationship between
Note and Tag
"""
note_tag = db.Table(
    'note_tag',
    db.Column(
        'note_id',
        db.Integer,
        db.ForeignKey('notes.id', ondelete="CASCADE")),
    db.Column(
        'tag_id',
        db.Integer,
        db.ForeignKey('tags.id', ondelete="CASCADE")))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(32))
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_date = db.Column(db.DateTime(), default=datetime.utcnow)

    notes = db.relationship(
        'Note', backref='author',
        lazy='dynamic', cascade="all, delete-orphan")
    notebooks = db.relationship(
        'Notebook', backref='author',
        lazy='dynamic', cascade="all, delete-orphan")

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py as f

        seed()
        for i in range(count):
            u = User(
                email=f.internet.email_address(),
                username=f.internet.user_name(True),
                password=f.lorem_ipsum.word(),
                confirmed=True)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha512')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()
        return True

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def generate_auth_token(self, expiration):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        json_user = {
            'url': url_for('api.get_note', id=self.id, _external=True),
            'username': self.username,
            'created_date': self.created_date,
            'notes': url_for('api.get_user_notes', id=self.id, _external=True),
            'note_count': self.notes.count()
        }
        return json_user

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class AnonymousUser(AnonymousUserMixin):

    def can(self):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class NoteQuery(BaseQuery, SearchQueryMixin):
    pass


class Note(db.Model):
    query_class = NoteQuery
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.id'))
    is_deleted = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)

    todo_items = db.relationship(
        "Todo", backref="note", cascade="all")
    tags = db.relationship(
        "Tag", secondary=note_tag,
        backref="Note", passive_deletes=True)

    # Full Text Search
    search_vector = db.Column(TSVectorType('title', 'body'))

    def to_json(self):
        json_note = {
            'url': url_for('api.get_note', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'created_date': self.created_date,
            'author': self.author_id,
        }
        return json_note

    def get_notebook(self, id):
        notebook = Notebook.query.filter_by(
            id=id).first()
        return notebook

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('note does not have a body')
        return Note(body=body)

    def _get_todo_items(self):
        return [todo for todo in self.todo_items]

    def _find_or_create_tag(self, tag):
        q = Tag.query.filter_by(tag=tag)
        t = q.first()
        if not (t):
            t = Tag(tag=tag.strip())
        return t

    def _get_tags(self):
        return [x.tag for x in self.tags]

    def _set_tags(self, value):
        while self.tags:
            del self.tags[0]
        for tag in value:
            self.tags.append(self._find_or_create_tag(tag))

    # simple wrapper for tags relationship
    str_tags = property(_get_tags,
                        _set_tags)


class Notebook(db.Model):
    __tablename__ = 'notebooks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    is_deleted = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    notes = db.relationship('Note', backref='notebook')

    def _show_notes(self):
        notes = []
        for note in self.notes:
            if note.is_deleted is False:
                notes.append(note)
        return notes


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(200))

    notes = db.relationship("Note", secondary=note_tag, backref="Tag")

    def _get_notes(self):
        notes = []
        for note in self.notes:
            if note.author == current_user and not note.is_deleted:
                notes.append(note)
        return notes


class Todo(db.Model):
    __tablename__ = 'todo_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    is_checked = db.Column(db.Boolean, default=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_date = db.Column(db.DateTime(), default=datetime.utcnow)
    checked_date = db.Column(db.DateTime())

    def get_note(self, id):
        note = Note.query.filter_by(
            id=id).first()
        return note

    @staticmethod
    def parse_markdown(markdown_body):
        checked = lambda x: "[x]" in x
        body = [line.encode('utf-8') for line in markdown_body.split("\n")]
        # pattern for a markdown todo-list ()
        pattern = re.compile(".*-\s" + "(\[[\sx]\]).*")
        todo_list = [line for line in body if pattern.match(line) is not None]
        for i, todo in enumerate(todo_list):
            delim = "\r"
            item = todo[todo.find(']') + 1:]
            found = item.find(delim)
            if found != -1:
                item = item[:found]
            todo_list[i] = (item, checked(todo))
        return todo_list

    @staticmethod
    def add_id_to_li_element(li, id):
        li = li.encode('utf-8')
        root = etree.fromstring(li.strip(), etree.HTMLParser())
        elem = root[0][0]
        elem.attrib["id"] = id
        new_li = etree.tostring(elem, method="html")
        new_li = unicode(new_li, "utf-8")
        return new_li

    @staticmethod
    def get_todo_item_id(li, todo_objs):
        li = li.encode("utf-8")
        element = html.fromstring(li.strip())
        todo_item = element.text_content()
        for item in todo_objs:
            if item.title == todo_item:
                return item.id
        return -1

    @staticmethod
    def toggle_checked_property_markdown(markdown_body, item):
        checked = lambda x: "[x]" in x
        body = [line.encode('utf-8') for line in markdown_body.split("\n")]
        # pattern for a markdown todo-list ()
        pattern = re.compile(".*-\s" + "(\[[\sx]\]).*")
        for i, line in enumerate(body):
            if pattern.match(line) is not None and item in line:
                if (checked(line)):
                    new_line = line.replace("[x]", "[ ]")
                else:
                    new_line = line.replace("[ ]", "[x]")
                body[i] = new_line
        new_body = "\n".join(body)
        new_body = unicode(new_body, "utf-8")
        return new_body
