import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
import smtplib
from email.mime.text import MIMEText
from email.header import Header

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('GET', 'POST'))
def index():
    message = session.get('user_id')
    return render_template('message.html', message=message)
