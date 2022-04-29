from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, StringField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job_title = StringField('Job Title')
    team_leader = StringField('Team Leader id')
    size = IntegerField('Work Size')
    collaborators = StringField('Collaborators')
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')