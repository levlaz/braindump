from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField, HiddenField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

class NoteForm(Form):
    title = StringField('Title:', validators=[Required()])
    body = TextAreaField('Dump Your Brain:', validators=[Required()])
    body_html = TextAreaField()
    tags = StringField()
    submit = SubmitField('Submit')

class ShareForm(Form):
    recipient_email = StringField('Recipient Email', validators=[Required()])
    submit = SubmitField('Share')
