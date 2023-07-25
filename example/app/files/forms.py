from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    from flask_wtf.file import FileRequired
    file = FileField('file', validators=[FileRequired()])