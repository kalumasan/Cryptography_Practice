
from flask import Flask, render_template, request, redirect, url_for, flash
from app.file_models.models import File
from app.user.models import User

from app.blueprints import shared_files




@shared_files.route('/')
def get__():
    
    files = File.query.filter(File.shared).all()
    users = list(User.get_by(id=file.creator_id) for file in files)
    list_ = list((file.filename, user.name) for file, user in zip(files, users))
    return render_template('shared_files.html', list=list_)


@shared_files.route('/download')
def get__download():
    
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        username = request.args.get('username')
        assert username, 'missing username'
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'signature'), 'unknown type'
        user = User.get_by(name=username)
        return File.download_file(user, filename, type_)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)
        return redirect('/shared_file')