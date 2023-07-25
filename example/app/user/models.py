# -*- coding: UTF-8 -*-
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime

from app.extensions import db
from app.extensions import bcrypt
from flask_sqlalchemy import SQLAlchemy
import enum
from sqlalchemy import Column, String, Integer, LargeBinary

from flask import current_app

class UserRole(enum.Enum):
    ADMIN = 'Administrator'
    USERS = 'Normal users'


# user models
class User(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    encrypted_symmetric_key = db.Column(db.LargeBinary(32), nullable=False, server_default='')
    encrypted_private_key = db.Column(db.LargeBinary(32), nullable=False, server_default='')
    encrypted_public_key = db.Column(db.LargeBinary(32), nullable=False, server_default='')
    created_time = db.Column(db.DateTime, default=datetime.now)
    

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def __repr__(self):
        return "<User %r>" % self.name
    

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create_user(cls, username,email,password):
        import app.secret
        user = User.get_by(name=username)
        assert user is None, 'email already registered'
        # 先随机生成一个用户的对称密钥与公私钥
        symmetric_key = app.secret.new_symmetric_key()
        private_key, public_key = app.secret.new_pair()
        print(symmetric_key)
        # 再用服务器的公钥加密这些密钥
        user = User(name=username,
                    email=email,
                    email_confirmed=True,                    
                    role=UserRole.ADMIN,
                    encrypted_symmetric_key=app.secret.encrypt(symmetric_key),
                    encrypted_private_key=app.secret.encrypt(private_key),
                    encrypted_public_key=app.secret.encrypt(public_key)
                    )
        user.password = password
        db.session.add(user)
        db.session.commit()
    

    
   