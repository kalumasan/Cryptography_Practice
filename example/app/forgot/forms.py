from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email,Regexp,Length,ValidationError


class EmailForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    


class CaptchaForm(FlaskForm):    
    verify_code = PasswordField('验证码', validators=[DataRequired()])


class ResetpswdForm(FlaskForm):    
    newpassword = PasswordField('密码', validators=[DataRequired()])
