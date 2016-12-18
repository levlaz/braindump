import hashlib

from app import login_manager, db
from app.model.shared import SharedNote
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for, jsonify
from flask_login import UserMixin, current_user, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from app.exceptions import ValidationError
from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

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
    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False)
    avatar_hash = db.Column(db.String(32))
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_date = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime(), default=datetime.utcnow)

    notes = db.relationship(
        'Note', backref='author',
        lazy='dynamic', cascade="all, delete-orphan")
    notebooks = db.relationship(
        'Notebook', backref='author',
        lazy='dynamic', cascade="all, delete-orphan")
    shared_notes = db.relationship(
        'SharedNote', backref="author",
        lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    def get_deleted_notes(self):
        """ Return all notes owned by this user that are in the trash."""
        return list(filter(lambda note: note.is_deleted, self.notes))

    # TODO move this to test mocks
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py as f

        seed()
        for i in range(count):
            u = User(
                email=f.internet.email_address(),
                password=f.lorem_ipsum.word(),
                confirmed=True)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

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

    def generate_auth_token(self):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=3600)
        return s.dumps({'id': self.id})

    def log_login(self):
        self.last_login_date = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return None

    def to_json(self):
        json_user = {
            'url': url_for('api.get_note', id=self.id, _external=True),
            'created_date': self.created_date,
            'notes': url_for('api.get_user_notes', id=self.id, _external=True),
            'note_count': self.notes.count()
        }
        return json_user


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
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebooks.id'))
    is_deleted = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)

    tags = db.relationship(
        "Tag", secondary=note_tag,
        backref="Note", passive_deletes=True)

    # Full Text Search
    search_vector = db.Column(TSVectorType('title', 'body'))

    def to_json(self):
        json_note = {
            'id': self.id,
            #'url': url_for('api.get_note', id=self.id, _external=True),
            'body': self.body,
            #'created_date': self.created_date,
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
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_date = db.Column(db.DateTime(), default=datetime.utcnow)

    notes = db.relationship(
        'Note', backref='notebook',
        lazy='dynamic')

    def active_notes(self):
        return list(filter(lambda note: (
            not note.is_deleted and not note.is_archived), self.notes))

    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'is_deleted': self.is_deleted,
            'author': self.author_id,
            'notes': list(map(lambda note: note.to_json(), self.notes.all())),
            'uri': url_for('api.notebook', notebook_id=self.id)
        }
        return json


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(200))

    notes = db.relationship("Note", secondary=note_tag, backref="Tag")

    def _get_notes(self):
        return list(filter(lambda x: (
            x.author == current_user and not x.is_deleted), self.notes))
