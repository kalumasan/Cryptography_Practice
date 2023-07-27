# -*- coding: UTF-8 -*-
from flask import render_template, redirect, send_from_directory, current_app,make_response
from flask_login import login_required

from app.blueprints import home


@home.route('/')
@login_required
def index():
    return render_template('home.html')

@home.route('public_key')
def public_key():
    from app.secret import get_pk_raw
    response = make_response(get_pk_raw())
    response.headers['Content-Disposition'] = 'attachment; filename=public_key'
    return response




@home.route('/images/<image_name>')
def images(image_name):
    try:
        return send_from_directory(current_app.config["UPLOAD_FOLDER"],
                                   path=image_name)
    except FileNotFoundError:
        abort(404)
