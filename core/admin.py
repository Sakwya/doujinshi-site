import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from core.urls import init_dic

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('GET', 'POST'))
def index():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect("user.route")
    url_dic = init_dic("ADMIN")
    url_dic.update({
        "review_cover": url_for("static", filename="img/admin/review.jpg"),
        "review": url_for("admin.review"),
    })
    return render_template('admin.html', **url_dic)


@bp.route('/review', methods=('GET', 'POST'))
def review():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for("user.route"))

    db = get_db()
    review_info_list = db.execute(
        "SELECT review_id, doujinshi_name FROM unconfirmed "
        "WHERE condition = 0",
        ()
    ).fetchall()
    for review_info in review_info_list:
        for i in review_info:
            print(i, end=" ")
        print()
    url_dic = init_dic("REVIEW")
    url_dic.update({
        'review_info_list': review_info_list,
    })
    print(url_dic)
    return render_template('review.html', **url_dic)


@bp.route('/review/<review_id>', methods=('GET', 'POST'))
def review_doujinshi(review_id):
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for("user.route"))

    db = get_db()
    unconfirmed_info = db.execute(
        "SELECT * FROM unconfirmed "
        "WHERE review_id = ?",
        (review_id,)
    ).fetchall()
    if unconfirmed_info.__len__() == 0:
        flash("无效的审核号")
        return redirect(url_for('admin.review'))
    author_id, class_id, user_id, doujinshi_name, doujinshi_cover, market, pages, condition = unconfirmed_info[0][1:]

    if author_id is None:
        author_name = "未知"
        author_page = ""
    else:
        author_name = db.execute(
            "SELECT author_name FROM author WHERE author_id = ?",
            (author_id,)
        ).fetchone()[0]
        author_page = "1"

    class_name = db.execute(
        "SELECT class_name FROM class "
        "WHERE class_id = ?",
        (class_id,)
    ).fetchone()[0]
    print(doujinshi_cover)
    if doujinshi_cover is None:
        doujinshi_cover = url_for('static', filename="review/no_cover.png")
    else:
        doujinshi_cover = url_for('static', filename='/review/cover/' + doujinshi_cover)

    if pages is None:
        pages = "未知"

    url_dic = init_dic("审核:" + review_id)
    url_dic.update({
        'author_name': author_name,
        'author_page': author_page,
        'class_id': class_id,
        'user_id': user_id,
        'doujinshi_name': doujinshi_name,
        'doujinshi_cover': doujinshi_cover,
        'market': market,
        'pages': pages,
        'condition': condition,
    })
    return render_template('review_doujinshi.html', **url_dic)
