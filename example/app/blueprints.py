# -*- coding: UTF-8 -*-
from flask import Blueprint

home = Blueprint('home', 'app.public.views', url_prefix='/')

auth = Blueprint('auth', 'app.auth.views', url_prefix='/auth')

forgot = Blueprint('forgot', 'app.forgot.views', url_prefix='/forgot')

files = Blueprint('files', 'app.files.views', url_prefix='/files')

shared_files = Blueprint('shared_files', 'app.shared_files.views', url_prefix='/shared_files')




all_blueprints = (
    home,
    auth,
    forgot,
    files,
    shared_files,
)
