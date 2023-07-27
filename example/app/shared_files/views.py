
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from app.file_models.models import File
from app.user.models import User

from app.blueprints import shared_files




@shared_files.route('/')
def get__():
    
    files = File.query.filter(File.shared).all()
    users = list(User.get_by(id=file.creator_id) for file in files)
    list_ = list((file.filename, user.name) for file, user in zip(files, users))
    return render_template('shared_files.html', list=list_)


@shared_files.route('/download',methods=['GET', 'POST'])
def get__download():
    
    try:
        filename = request.args.get('filename')
        assert filename, 'missing filename'
        username = request.args.get('username')
        assert username, 'missing username'
        type_ = request.args.get('type')
        assert type_, 'missing type'
        assert type_ in ('encrypted', 'signature','plaintext'), 'unknown type'
        user = User.get_by(name=username)        
        return File.download_shared_file_out(user, filename, type_)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)
        return redirect(url_for('shared_files'))



@shared_files.route('/verify_download',methods=['POST'])
def verify_download():
    # 从 POST 请求中获取前端发送的 JSON 数据
    data = request.get_json()

    # 从 JSON 数据中提取用户输入的密码
    password = data.get('password')
    username = data.get('username')
    password_stripped = password[2:-1]

    user = User.get_by(name=username)
    encrypted_symmetric_key=user.encrypted_symmetric_key

    # 删除前缀'b'并将其转换为字符串
    key_data = repr(encrypted_symmetric_key)[2:-1]

    if password_stripped==key_data:
        return jsonify({ "valid": True })
    else:
        return jsonify({ "valid": False })
