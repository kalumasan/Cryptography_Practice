from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required,current_user
from flask import Blueprint
from flask_login import login_required
from app.file_models.models import File
from app.user.models import User
from app.extensions import db
from app.blueprints import files
from app.files.forms import FileForm
from app.extensions import login_manager

@files.route('/')
@login_required
def get__file():
    
    files = File.query.filter(File.creator_id == current_user.id).all()
    return render_template('file.html', username=current_user.name, files=files)


@files.route('/upload')
@login_required
def get__upload():
    return render_template('files/upload.html', form=FileForm())


@files.route('/upload', methods=['POST'])
@login_required
def post__upload():
    try:
        
        form = FileForm()
        assert form.validate_on_submit(), 'invalid form fields'
        data = form.file.data
        File.upload_file(current_user, data)
        flash('上传成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('上传失败！'+message)
    return redirect('/files')


@files.route('/remove')
@login_required
def get__remove():
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        File.delete_file(current_user, filename)
        flash('删除成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('删除失败！'+message)
    return redirect('/files')


@files.route('/download')
@login_required
def get__download():
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'plaintext', 'signature', 'hashvalue'), 'unknown type'
        return File.download_file(current_user, filename, type_)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！'+message)
        return redirect('/files')


@files.route('/share',methods=['GET', 'POST'])
@login_required
def get__share():
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'

        expire_time_str = request.form.get('expire_time', None)  # 默认有效期为0，表示不设置时间限制
        if expire_time_str=='5分钟':
            expire_time=300
        elif expire_time_str=='1小时':
            expire_time=3600
        elif expire_time_str=='24小时':
            expire_time=86400
        elif expire_time_str=='不限时':
            expire_time=None
        else:
            expire_time=0
        max_downloads = int(request.form.get('max_downloads', 0))  # 默认下载次数限制为0，表示不设置次数限制
        File.share_file(current_user, filename, expire_time, max_downloads)
        flash('设置成功！')
        return redirect('/files')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('设置失败！'+message)
        return redirect('/files')
    
@files.route('/shared_files')
@login_required
def get_shared_files():
        
    files = File.query.filter(File.shared).all()
    users = list(User.get_by(id=file.creator_id) for file in files)
    list_ = list((file.filename, user.name) for file, user in zip(files, users))
    return render_template('files/share.html', list=list_)


@files.route('/shared_files_download',methods=['GET', 'POST'])
@login_required
def shared_files_download():    
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        username = request.args.get('username')
        assert username, 'missing username'
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'signature','plaintext'), 'unknown type'
        user = User.get_by(name=username)
        
        return File.download_shared_file(user, filename, type_)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)
        return redirect(url_for('files.shared_files'))