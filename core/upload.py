from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core import app
from core.db import get_db
from core.urls import init_dic
import random

bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/', methods=('GET', 'POST'))
def upload():
    if session.get('user_id') is None:
        flash("请先进行登录！")
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        db = get_db()
        sql = "INSERT INTO unconfirmed (author_name,type_id,uploader_id,doujinshi_name,doujinshi_cover,market,pages" \
              ") VALUES (?,?,?,?,?,?,?)"

        author_name = request.form['author_name']
        if len(author_name) != 0:
            sql = sql.replace('?', author_name, 1)
        else:
            sql = sql.replace('author_name,', '').replace(',?', '', 1)

        type_id = request.form['type_id']
        sql = sql.replace('?', type_id, 1)

        uploader_id = session.get('user_id')
        sql = sql.replace('?', str(uploader_id), 1)

        doujinshi_name = request.form['doujinshi_name']
        sql = sql.replace('?', '"' + doujinshi_name + '"', 1)

        cover = request.files['doujinshi_cover']
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
            sql = sql.replace(',market', '').replace(',?', '', 1)

        pages = request.form['pages']
        if len(pages) != 0:
            sql = sql.replace('?', pages, 1)
        else:
            sql = sql.replace(',pages', '').replace(',?', '', 1)
        print(sql)
        db.execute(sql)
        ans = db.commit()
        flash("提交成功！")
        print(ans)
        return redirect(url_for('upload.upload'))

    db = get_db()
    url_dic = init_dic()

    results = db.execute(
        "SELECT author_name FROM author",
        ()
    ).fetchall()
    author_list = []
    for result in results:
        author_list.append(result[0])

    url_dic.update({
        'authors': author_list,
    })
    return render_template('upload.html', **url_dic)
