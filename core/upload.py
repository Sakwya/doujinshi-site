from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core import app
from core.db import get_db
from core.operate import insert_unconfirmed
from core.urls import init_dic
import random

bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/', methods=('GET', 'POST'))
def upload():
    user_id = session.get('user_id')
    if user_id is None:
        flash("请先进行登录！")
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        type_id = request.form['type_id']
        uploader_id = user_id
        doujinshi_name = request.form['doujinshi_name']

        doujinshi_cover = None
        cover = request.files['doujinshi_cover']
        if len(cover.filename) != 0:
            doujinshi_cover = doujinshi_name + str(random.random())[3:8] + '.' + cover.filename.split('.')[-1]
            cover.save('core/static/review/cover/' + doujinshi_cover)

        author_name = request.form['author_name']
        if len(author_name) == 0:
            author_name = None

        market = request.form['market']
        if len(market) == 0:
            market = None

        pages = request.form['pages']
        if len(pages) == 0:
            pages = None

        adult = request.form['class']
        if len(adult) == 0:
            adult = None

        tag_list = request.form['tag_list']
        if len(tag_list) == 0:
            tag_list = None

        response = insert_unconfirmed({
            'type_id': type_id,
            'doujinshi_name': doujinshi_name,
            'author_name': author_name,
            'market': market,
            'pages': pages,
            'class': adult,
            'doujinshi_cover': doujinshi_cover,
            'uploader_id': uploader_id,
            'tag_list': tag_list,
        })
        if response == 0:
            flash("提交成功！")
            return redirect(url_for('user.route'))
        elif response == -1:
            flash("传值错误")
            return redirect(url_for('upload.upload'))
        elif response == -2:
            flash("提交失败")
            return redirect(url_for('upload.upload'))
        return Exception

    db = get_db()
    url_dic = init_dic()

    results = db.execute(
        "SELECT author_name FROM author",
        ()
    ).fetchall()
    author_list = []

    for result in results:
        author_list.append(result[0])

    results = db.execute(
        "SELECT tag_name FROM tag_in_order",
        ()
    ).fetchall()
    tag_list = []

    for result in results:
        tag_list.append(result[0])

    url_dic.update({
        'authors': author_list,
        'tags': tag_list
    })
    return render_template('upload.html', **url_dic)
