from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash

from core.db import get_db
from core.urls import init_dic
from core.fetch import get_collection, get_by_uploader, get_username, get_by_author
import random

bp = Blueprint('author', __name__, url_prefix='/author')


@bp.route('/<author_id>')
def page(author_id):
    if session.get('user_id') is None:
        flash("请先进行登录")
        return redirect(url_for('user.login'))
    db = get_db()
    author_name = db.execute(
        "SELECT author_name FROM author WHERE author_id= ? "
        "LIMIT 1",
        (author_id,)
    ).fetchone()
    if author_name is None:
        flash('作者不存在')
        return redirect(url_for('manga'))
    author_name = author_name[0]
    print(author_name)

    artwork_num = db.execute(
        "SELECT COUNT(*) FROM doujinshi "
        "WHERE author_id = ?",
        (author_id,)
    ).fetchone()[0]

    url_dic = init_dic('作者:' + author_name)

    url_dic.update({
        'author_name':author_name,
        'doujinshi_num': artwork_num,
        'doujinshi_list': get_by_author(author_id),
    })
    print(url_dic)
    return render_template('author.html', **url_dic)

