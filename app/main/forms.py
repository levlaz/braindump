from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import Required, Length, Email

def validate_tags(form, field):
    if field.data:
        for x in field.data.split(','):
            if len(x) not in range(200+1):
                raise ValidationError('All tags must be less than 200 characters')

class NoteForm(Form):
    title = StringField('Title:', validators=[Required(), Length(1, 200)])
    body = TextAreaField('Dump Your Brain:', validators=[Required()])
    body_html = TextAreaField()
    tags = StringField(validators=[validate_tags])
    notebook = SelectField(coerce=int)
    submit = SubmitField('Submit')


class ShareForm(Form):
    recipient_email = StringField('Recipient Email', validators=[Required(), Length(1, 254), Email()])
    submit = SubmitField('Share')


class NotebookForm(Form):
    title = StringField('Title:', validators=[Required(), Length(1, 200)])
    submit = SubmitField('Submit')


class SearchForm(Form):
    search_field = StringField()
    submit = SubmitField('Search')
