from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user,current_user
from flask import Blueprint
from flask_login import login_required
from app.file_models.models import File
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


@files.route('/share')
@login_required
def get__share():
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        File.share_file(current_user, filename)
        flash('设置成功！')
        return redirect('/files')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('设置失败！'+message)
        return redirect('/files')