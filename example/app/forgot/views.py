from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask import Blueprint
from app.forgot.forms import EmailForm,CaptchaForm,ResetpswdForm
from app.user.models import User,UserRole
from app.extensions import db
from app.blueprints import forgot
import random
import re
import os
import hashlib



username_pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]+')
password_pattern = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,36}')


@forgot.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    from app.application import flask_app
    mail=Mail(flask_app)
    form=EmailForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return "邮箱不存在"
        else:
            email=form.email.data       
            token = random.randint(100000, 999999)  # 生成随机验证码
            msg = Message('Email Verification', sender='getuplate_crypt@163.com', recipients=[email])
            msg.body = f'Your verification token is: {token}'
            mail.send(msg)
            return redirect(url_for('forgot.verify_email',token=token, email=form.email.data))
    
    return render_template('forgot/e_mail.html',form=form)


@forgot.route('/verify_email/<token>/<email>',methods=['GET', 'POST'])
def verify_email(token,email):
    form=CaptchaForm()
    t_oken=token
    e_mail=email
    if form.validate_on_submit():
        if t_oken==form.verify_code.data:            
            return redirect(url_for('forgot.reset_password', email=e_mail))
        else:
            flash('无效的验证令牌。')
            return redirect(url_for('auth.login'))
    
    return render_template('forgot/verify.html',form=form,token=t_oken,email=e_mail)



@forgot.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    form=ResetpswdForm()    
    user = User.query.filter_by(email=email).first()
    if form.validate_on_submit():
        #if form.validate():
        # 实际应用中，这里可以重置用户的密码
        try:
            newpswd=form.newpassword.data
            assert password_pattern.fullmatch(newpswd), '密码不安全,同时包含至少一个小写字母,一个大写字母和一个数字,长度8-36'
            salt = os.urandom(16)
        # 加密密码
            hashed_password = hashlib.pbkdf2_hmac('sha256', newpswd.encode('utf-8'), salt, 100000, 64)
            user.password = hashed_password
            db.session.commit()
            flash('密码重置成功！')
            return redirect(url_for('auth.login'))
        #else:
        except AssertionError as e:
            flash('密码不安全，密码重置失败！')
            return redirect(url_for('forgot.reset_password',email=email))
    return render_template('forgot/reset_password.html', form=form,email=email)    