from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class DepartmentForm(FlaskForm):
    title = StringField('Department title', validators=[DataRequired()])
    chief = StringField('Id of the Chief of the Department', validators=[DataRequired()])
    members = StringField('Id members of the Department', validators=[DataRequired()])
    email = EmailField('Email of the Department', validators=[DataRequired()])
    submit = SubmitField('Add Department')