import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
from core.urls import init_dic

bp = Blueprint('doujinshi', __name__, url_prefix='/doujinshi')


@bp.route('/', methods=('GET', 'POST'))
def home():
    url_dic = init_dic('DoujinshiClub')
    db = get_db()
    results = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover FROM doujinshi "
    ).fetchmany(15)
    doujinshis = []
    for result in results:
        doujinshi = [result[1], url_for('doujinshi.index', doujinshi_id=result[0])]
        if result[2] is None:
            doujinshi.append(url_for('static', filename='no_cover.jpg'))
        doujinshis.append(doujinshi)
    url_dic.update({
        'doujinshis': doujinshis,
    })
    return render_template("doujinshi.html", **url_dic)


@bp.route('/<doujinshi_id>', methods=('GET', 'POST'))
def index(doujinshi_id):
    user_id = session.get('user_id')
    if user_id == 'none':
        flash('请先进行登陆！')
        return redirect(url_for('user.login'))
    db = get_db()
    result = db.execute(
        "SELECT doujinshi_name,author_id,class_id,user_id,doujinshi_cover,market,pages FROM doujinshi "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    ).fetchone()
    if result is None:
        flash("找不到该页面")
        return redirect(url_for('doujinshi.home'))
    doujinshi_name, author_id, class_id, user_id, doujinshi_cover, market, pages = result
    class_name = db.execute(
        "SELECT class_name FROM class "
        "WHERE class_id = ?",
        (class_id,)
    ).fetchone()[0]
    url_dic = init_dic("")
    url_dic.update({
        'doujinshi_id': doujinshi_id,
        'doujinshi_name': doujinshi_name,
        'author_id': author_id,
        'class': class_name,
        'doujinshi_cover': doujinshi_cover,
        'market': market,
        'pages': pages,
    })

    return render_template("artwork.html", **url_dic)
