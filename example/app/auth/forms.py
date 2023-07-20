# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email,Regexp,Length,ValidationError


class SignInForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField('用户名', validators=[ DataRequired('用户名不能为空'),Regexp('^[\u4e00-\u9fa5a-zA-Z0-9-_.]+$', message='用户名只能包含中文、英文字母、数字、连字符、下划线和句点。')])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])


class EmailForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    captcha = PasswordField('验证码', validators=[DataRequired()])
