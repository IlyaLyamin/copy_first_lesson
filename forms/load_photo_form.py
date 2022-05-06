from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from flask_wtf.file import FileAllowed


class UserPhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Отправить')