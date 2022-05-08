from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from flask_wtf.file import FileAllowed, FileRequired


class GaleryForm(FlaskForm):
    photo = FileField('Photo', validators=[FileAllowed(['png', 'jpg'], FileRequired())])
    submit = SubmitField('Отправить')