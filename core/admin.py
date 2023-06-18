import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
import os
from shutil import copyfile
from core.db import get_db
from core.urls import init_dic
from core.fetch import get_username

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def index():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect("user.route")
    url_dic = init_dic()
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
    info = db.execute(
        "SELECT type_id, review_id, doujinshi_name, uploader_id FROM unconfirmed "
        "WHERE condition = 0",
        ()
    ).fetchall()
    ban_num = db.execute(
        "SELECT COUNT(*) FROM unconfirmed "
        "WHERE condition = -1"
    ).fetchone()[0]
    confirmed_num = db.execute(
        "SELECT COUNT(*) FROM unconfirmed "
        "WHERE condition = 1"
    ).fetchone()[0]
    unconfirmed_num = len(info)
    type_list = ["未知", "漫画", "画册", "同人文", "刊物"]
    unconfirmed_list = []
    for piece in info:
        pieces = [type_list[piece[0]], piece[1], piece[2], get_username(piece[3]),
                  url_for('admin.review_doujinshi', review_id=piece[1])]
        unconfirmed_list.append(pieces)
    url_dic = init_dic("REVIEW")
    url_dic.update({
        'ban_num': ban_num,
        'confirmed_num': confirmed_num,
        'unconfirmed_num': unconfirmed_num,
        'unconfirmed_list': unconfirmed_list,
    })
    return render_template('review.html', **url_dic)


@bp.route('/review/<review_id>', methods=('GET', 'POST'))
def review_doujinshi(review_id):
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for("user.route"))

    db = get_db()
    if request.method == 'POST':
        sql = "INSERT INTO doujinshi (author_id,type_id,uploader_id,doujinshi_name,doujinshi_cover,market,pages" \
              ") VALUES (?,?,?,?,?,?,?)"
        author_name = request.form['author_name']
        if len(author_name) != 0:
            author_id = db.execute(
                "SELECT author_id FROM author "
                "WHERE author_name =?",
                (author_name,)
            ).fetchone()
            if author_id is None:
                db.execute("INSERT INTO author(author_name) VALUES (?)", (author_name,))
                db.commit()
                author_id = db.execute(
                    "SELECT author_id FROM author "
                    "WHERE author_name =?",
                    (author_name,)
                ).fetchone()
            sql = sql.replace('?', str(author_id[0]), 1)
        else:
            sql = sql.replace('author_id,', '').replace(',?', '', 1)

        type_id = request.form['type_id']
        sql = sql.replace('?', type_id, 1)

        uploader_id = request.form['uploader_id']
        sql = sql.replace('?', str(uploader_id), 1)

        doujinshi_name = request.form['doujinshi_name']
        sql = sql.replace('?', '"' + doujinshi_name + '"', 1)

        cover_type = request.form['cover_type']

        if cover_type == "0":
            review_id = request.form['review_id']
            doujinshi_cover = db.execute(
                "SELECT doujinshi_cover FROM unconfirmed "
                "WHERE review_id = ?",
                (review_id,)
            ).fetchone()[0]
            if doujinshi_cover is None:
                sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)
            else:
                old_path = os.getcwd() + '\\core\\static\\review\\cover\\' + doujinshi_cover
                doujinshi_cover = doujinshi_name + '.' + doujinshi_cover.split('.')[-1]
                new_path = os.getcwd() + '\\core\\static\\img\\cover\\' + doujinshi_cover
                copyfile(old_path, new_path)
                sql = sql.replace('?', '"' + doujinshi_cover + '"', 1)

        if cover_type == "1":
            sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)
        if cover_type == "2":
            cover = request.files['doujinshi_cover']
            if len(cover.filename) != 0:
                doujinshi_cover = doujinshi_name + '.' + cover.filename.split('.')[-1]
                cover.save('core/static/review/cover/' + doujinshi_cover)
                sql = sql.replace('?', '"' + doujinshi_cover + '"', 1)
            else:
                sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)

        print(sql)
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
        try:
            db.execute(sql)
            db.execute(
                "UPDATE unconfirmed "
                "SET condition = 1 "
                "WHERE review_id = ?",
                (review_id,)
            )
            db.commit()
            flash("提交成功")
            return redirect(url_for('admin.review'))
        except ValueError:
            flash("发生错误")
            return redirect(url_for('admin.review', review_id=review_id))

    unconfirmed_info = db.execute(
        "SELECT * FROM unconfirmed "
        "WHERE review_id = ?",
        (review_id,)
    ).fetchall()
    if unconfirmed_info.__len__() == 0:
        flash("无效的审核号")
        return redirect(url_for('admin.review'))
    author_name, type_id, uploader_id, doujinshi_name, doujinshi_cover, market, pages, condition = unconfirmed_info[0][
                                                                                                   1:]

    if doujinshi_cover is None:
        doujinshi_cover = url_for('static', filename="review/no_cover.png")
    else:
        doujinshi_cover = url_for('static', filename='review/cover/' + doujinshi_cover)

    if market is None:
        market = ""
    if pages is None:
        pages = ""

    results = db.execute(
        "SELECT author_name FROM author",
        ()
    ).fetchall()
    author_list = []
    for result in results:
        author_list.append(result[0])

    url_dic = init_dic("审核作品:" + review_id)
    url_dic.update({
        'review_id': review_id,
        'authors': author_list,
        'author_name': author_name,
        'type_id': type_id,
        'uploader_id': uploader_id,
        'doujinshi_name': doujinshi_name,
        'doujinshi_cover': doujinshi_cover,
        'market': market,
        'pages': pages,
        'condition': condition,
    })
    return render_template('review_doujinshi.html', **url_dic)


@bp.route('/review/ban', methods=('GET', 'POST'))
def ban():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for("user.route"))
    if request.method == 'POST':
        db = get_db()
        review_id = request.form['review_id']
        try:
            db.execute(
                "UPDATE unconfirmed "
                "SET condition = -1 "
                "WHERE review_id = ?",
                (review_id,)
            )
            db.commit()
            flash("删除成功")
            return redirect(url_for("admin.review"))
        except ValueError:
            flash("发生错误")
            return redirect(url_for("admin.review", review_id=review_id))
    return redirect(url_for("admin.review"))
