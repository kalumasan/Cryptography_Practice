from sqlalchemy import and_
from os import remove, path, mkdir
import re
from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime

from app.extensions import db
from app.extensions import bcrypt

import enum
from config import storage_path
from flask import current_app,flash,redirect,url_for
import app.secret




filename_pattern = re.compile(r'[^\u4e00-\u9fa5]+')


class File(db.Model):
    __tablename__ = 'files'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    filename = db.Column(db.String(64), primary_key=True)
    hash_value = db.Column(db.String(128))
    shared = db.Column(db.Boolean, default=False)
    download_tokens = db.Column(db.String(36),nullable=True)
    expire_time = db.Column(db.Integer)  # 存储时间戳，单位为秒
    max_downloads = db.Column(db.Integer)
    __unique_constraint__ = (creator_id, filename)  # 添加唯一约束，替代之前的复合主键

    @classmethod
    def upload_file(cls, user, data):
        from hashlib import sha512
        from config import allowed_file_suffix_list
        filename = data.filename
        assert len(filename) <= 64, 'filename too long (>64B)'
        assert filename_pattern.fullmatch(filename), 'no unicode character allowed'
        filename_suffix = filename.rsplit('.', maxsplit=1)[-1]
        print(f"filename_suffix: {filename_suffix}, allowed_file_suffix_list: {allowed_file_suffix_list}")
        assert filename_suffix in allowed_file_suffix_list, 'banned file type'
        
        f = File.query.filter(and_(File.creator_id == user.id, File.filename == filename)).first()
        assert not f, 'file already exists'
        content = data.read()
        assert len(content) < 1*1024*1024, 'file too large (>=10MB)'
        user_id = str(user.id)+'/'
        if not path.exists(storage_path+user_id):
            if not path.exists(storage_path):
                mkdir(storage_path)
            mkdir(storage_path+user_id)
        # 计算原文件的哈希
        hash_value = sha512(content).hexdigest()
        print(user.encrypted_symmetric_key)
        # 判断文件是否存在
        if not path.exists(storage_path+user_id+hash_value):
            # 加密并存储。加密前得先还原出对称密钥。
            content = app.secret.symmetric_encrypt(app.secret.decrypt(user.encrypted_symmetric_key), content)
            # 同时计算签名
            signature = app.secret.sign(content)
            # 保存密文与签名
            with open(storage_path+user_id+hash_value, 'wb') as f:
                f.write(content)
            with open(storage_path+user_id+hash_value+'.sig', 'wb') as f:
                f.write(signature)
        creator_id = user.id
        file = File(creator_id=creator_id, filename=filename, hash_value=hash_value)
        db.session.add(file)
        db.session.commit()

    @classmethod
    def delete_file(cls, user, filename):
        f = File.query.filter(and_(File.creator_id == user.id, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        db.session.delete(f)
        db.session.commit()
        files = File.query.filter(File.hash_value == hash_value).all()
        if not len(files):
            remove(storage_path+str(user.id)+'/'+hash_value)
            remove(storage_path+str(user.id)+'/'+hash_value+'.sig')

    @classmethod
    def download_file(cls, user, filename, type_):
        from flask import make_response
        f = File.query.filter(and_(File.creator_id == user.id, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        hash_value = f.hash_value
        if type_ == 'hashvalue':
            content = hash_value
            filename = filename + '.hash'
        elif type_ == 'signature':
            # 读取签名
            with open(storage_path+str(user.id)+'/'+hash_value+'.sig', 'rb') as f_:
                content = f_.read()
                filename = filename+'.sig'
        else:
            # 读取密文
            with open(storage_path+str(user.id)+'/'+hash_value, 'rb') as f_:
                content = f_.read()
            if type_ == 'plaintext':
                content = app.secret.symmetric_decrypt(app.secret.decrypt(user.encrypted_symmetric_key), content)
            elif type_ == 'encrypted':
                filename = filename + '.encrypted'
        response = make_response(content)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    @classmethod
    def share_file(cls, user, filename, expire_time=None, max_downloads=None):
        import uuid
        import time
        f = File.query.filter(and_(File.creator_id == user.id, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        f.shared = not f.shared
        if f.shared:
            f.download_tokens = str(uuid.uuid4())
            print(f.download_tokens)
            if expire_time is not None:
                f.expire_time = int(time.time()) + expire_time
            if max_downloads is not None:
                f.max_downloads = max_downloads
        db.session.commit()
        if not f.shared:
            f.download_tokens = None
            print(f.download_tokens)


    @classmethod
    def download_shared_file(cls, user, filename, type_):
        from flask import make_response
        import time
        f = File.query.filter(and_(File.creator_id == user.id, File.filename == filename)).first()
        assert f, 'no such file ({})'.format(filename)
        if not f.download_tokens:
            return redirect(url_for('files.get_shared_files', code=301)), flash('Invalid token')
        if f.expire_time is not None and time.time() > f.expire_time:
            return redirect(url_for('files.get_shared_files', code=301)), flash('Token has expired')
        if f.max_downloads is not None and f.max_downloads <= 0:
            return redirect(url_for('files.get_shared_files', code=301)), flash('Exceeded maximum download limit')
        hash_value = f.hash_value
        if type_ == 'hashvalue':
            content = hash_value
            filename = filename + '.hash'
        elif type_ == 'signature':
            # 读取签名
            with open(storage_path+str(user.id)+'/'+hash_value+'.sig', 'rb') as f_:
                content = f_.read()
                filename = filename+'.sig'
        else:
            # 读取密文
            with open(storage_path+str(user.id)+'/'+hash_value, 'rb') as f_:
                content = f_.read()
            if type_ == 'plaintext':
                content = app.secret.symmetric_decrypt(app.secret.decrypt(user.encrypted_symmetric_key), content)
            elif type_ == 'encrypted':
                filename = filename + '.encrypted'
        response = make_response(content)
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        if f.max_downloads is not None:
            f.max_downloads-=1
        db.session.commit()
        return response