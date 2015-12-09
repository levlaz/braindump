from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import Required


class NoteForm(Form):
    title = StringField('Title:', validators=[Required()])
    body = TextAreaField('Dump Your Brain:', validators=[Required()])
    body_html = TextAreaField()
    tags = StringField()
    notebook = SelectField(coerce=int)
    submit = SubmitField('Submit')


class ShareForm(Form):
    recipient_email = StringField('Recipient Email', validators=[Required()])
    submit = SubmitField('Share')


class NotebookForm(Form):
    title = StringField('Title:', validators=[Required()])
    submit = SubmitField('Submit')


class SearchForm(Form):
    search_field = StringField()
    submit = SubmitField('Search')
