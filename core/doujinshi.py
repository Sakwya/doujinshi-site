import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db

bp = Blueprint('doujinshi', __name__, url_prefix='/doujinshi')


@bp.route('/', methods=('GET', 'POST'))
def home():
    return render_template("doujinshi.html")


@bp.route('/<doujinshi_id>', methods=('GET', 'POST'))
def index(doujinshi_id):
    user_id = session.get('user_id')
    if user_id == 'none':
        flash('请先进行登陆！')
        return redirect(url_for('user.login'))

    return render_template("message.html", message=doujinshi_id)
