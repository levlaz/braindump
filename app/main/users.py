from datetime import datetime
from flask import render_template, redirect, \
    url_for, flash, abort, current_app, request, \
    jsonify
from flask_login import current_user, login_required

from . import main
from app import db, csrf


@main.route('/users', methods=['PUT'])
@login_required
def update_user():
    if request.is_json:
        current_user.default_notebook = request.json.get('default_notebook')
        db.session.commit()
        return jsonify(current_user.to_json())