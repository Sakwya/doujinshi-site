import functools
import random

from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core import app
from core.db import get_db
from core.urls import init_dic
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random

bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/', methods=('GET', 'POST'))
def upload():
    if session.get('user_id') is None:
        flash("请先进行登录！")
        return redirect(url_for('user.login'))
    if request.method == 'POST':
        pass

    db = get_db()
    url_dic = init_dic('UPLOAD')

    results = db.execute(
        "SELECT author_name FROM author",
        ()
    ).fetchall()
    author_list = []
    for result in results:
        author_list.append(result[0])

    results = db.execute(
        "SELECT * FROM class",
        ()
    ).fetchall()
    class_list = []
    for result in results:
        class_list.append([result[0], result[1]])
    url_dic.update({
        'authors': author_list,
        'classes': class_list,
    })
    return render_template('upload.html', **url_dic)


@bp.route('/doujinshi', methods=('GET', 'POST'))
def doujinshi():
    if session.get('user_id') is None:
        flash("请先进行登录！")
        return redirect(url_for('user.login'))
    if request.method == 'POST':
        db = get_db()
        sql = "INSERT INTO unconfirmed (author_id,class_id,user_id,doujinshi_name,doujinshi_cover,market,pages" \
              ") VALUES (?,?,?,?,?,?,?)"

        author_name = request.form['author']
        if len(author_name) != 0:
            author_id = db.execute(
                "SELECT author_id FROM author WHERE author_name = ?",
                (author_name,)
            ).fetchone()
            if author_id is None:
                db.execute(
                    "INSERT INTO author values(NULL,?)",
                    (author_name,)
                )
                author_id = db.execute(
                    "SELECT author_id FROM author WHERE author_name = ?",
                    (author_name,)
                ).fetchone()
            sql = sql.replace('?', str(author_id[0]), 1)
        else:
            sql = sql.replace('author_id,', '').replace(',?', '', 1)

        class_id = request.form['class']
        sql = sql.replace('?', class_id, 1)

        user_id = session.get('user_id')
        sql = sql.replace('?', str(user_id), 1)

        doujinshi_name = request.form['doujinshiname']
        sql = sql.replace('?', '"' + doujinshi_name + '"', 1)

        cover = request.files['cover']
        if len(cover.filename) != 0:
            ran = str(random.random())[3:8]
            cover.save(
                'core/static/review/cover/' + doujinshi_name + ran + '.' + cover.filename.split('.')[-1])
            sql = sql.replace('?', '"' + doujinshi_name + ran + '.' + cover.filename.split('.')[-1] + '"', 1)
        else:
            sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)

        market = request.form['market']
        if len(market) != 0:
            market = '"' + market + '"'
            sql = sql.replace('?', market, 1)
        else:
            sql = sql.replace('market,', '').replace(',?', '', 1)

        pages = request.form['pages']
        if len(pages) != 0:
            sql = sql.replace('?', pages, 1)
        else:
            sql = sql.replace(',pages', '').replace(',?', '', 1)
        print(sql)
        db.execute(sql)
        ans = db.commit()
        flash("提交成功！")
        return redirect(url_for('upload.upload'))