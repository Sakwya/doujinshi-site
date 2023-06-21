import os
from shutil import copyfile

from flask import Blueprint, request, render_template, flash, session, redirect, url_for

from core.db import get_db
from core.fetch import get_username
from core.operate import insert_doujinshi, get_doujinshi_id, create_doujinshi_url
from core.scripts.read_info import read_dlsite, not_exist, read_melonbooks
from core.urls import init_dic

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def index():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect("user.route")
    url_dic = init_dic()
    url_dic.update({
        "review_cover": url_for("static", filename="img/admin/review.jpg"),
        "batch_import_cover": url_for('static', filename="img/admin/import.jpg"),
        "batch_url_cover": url_for('static', filename="img/admin/url.jpg"),
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
        type_id = request.form['type_id']
        uploader_id = request.form['uploader_id']
        doujinshi_name = request.form['doujinshi_name']

        doujinshi_cover = None
        cover_type = request.form['cover_type']
        if cover_type == "0":
            doujinshi_cover = db.execute(
                "SELECT doujinshi_cover FROM unconfirmed "
                "WHERE review_id = ?",
                (review_id,)
            ).fetchone()[0]
            if doujinshi_cover is not None:
                old_path = os.getcwd() + '\\core\\static\\review\\cover\\' + doujinshi_cover
                doujinshi_cover = doujinshi_name + '.' + doujinshi_cover.split('.')[-1]
                new_path = os.getcwd() + '\\core\\static\\img\\cover\\' + doujinshi_cover
                copyfile(old_path, new_path)
        if cover_type == "1":
            pass
        if cover_type == "2":
            cover = request.files['doujinshi_cover']
            if len(cover.filename) != 0:
                doujinshi_cover = doujinshi_name + '.' + cover.filename.split('.')[-1]
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

        tag_list = request.form['tag_list']
        if tag_list is None:
            tag_list = []
        else:
            tag_list = tag_list.split('#')
            tag_list.remove('')

        class_ = request.form['class']
        if len(class_) == 0:
            class_ = None

        print(tag_list)
        response = insert_doujinshi({
            'type_id': type_id,
            'doujinshi_name': doujinshi_name,
            'author_name': author_name,
            'market': market,
            'pages': pages,
            'tag_list': tag_list,
            'class': class_,
            'doujinshi_cover': doujinshi_cover,
            'uploader_id': uploader_id,
        })
        if response == 0:
            flash("提交成功")
            db.execute(
                "UPDATE unconfirmed SET condition = 1 "
                "WHERE review_id = ?",
                (review_id,)
            )
            db.commit()
            return redirect(url_for('admin.review'))
        elif response == -1:
            flash("传值错误")
            return redirect(url_for('admin.review', review_id=review_id))
        elif response == -2:
            flash("提交失败")
            return redirect(url_for('admin.review', review_id=review_id))
        return Exception
    unconfirmed_info = db.execute(
        "SELECT * FROM unconfirmed "
        "WHERE review_id = ?",
        (review_id,)
    ).fetchone()
    if unconfirmed_info is None:
        flash("无效的审核号")
        return redirect(url_for('admin.review'))
    author_name, type_id, uploader_id, doujinshi_name, doujinshi_cover, market, pages, tag_list, class_, condition = \
        unconfirmed_info[1:]

    if doujinshi_cover is None:
        doujinshi_cover = url_for('static', filename="review/no_cover.png")
    else:
        doujinshi_cover = url_for('static', filename='review/cover/' + doujinshi_cover)

    if market is None:
        market = ""
    if pages is None:
        pages = ""
    if tag_list is None:
        tag_list = []
    else:
        tag_list = tag_list.split('#')
        tag_list.remove('')

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
        'tag_list': tag_list,
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


@bp.route('/batch_import', methods=('GET', 'POST'))
def batch_import():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for("user.route"))

    if request.method == 'POST':
        type_id = request.form['type_id']
        site = request.form['site']
        print(site,type_id)
        if site == '1':
            dlsite = read_dlsite()
            dlsite = not_exist(dlsite)
            for info_dic in dlsite:
                n_type_id = str(info_dic['type_id'])
                if n_type_id == type_id:
                    response = insert_doujinshi(info_dic)
                    if response == -1:
                        flash("传值错误")
                        break
                    elif response == -2:
                        flash("提交失败")
                        break
        if site == '2':
            melonbooks = read_melonbooks()
            melonbooks = not_exist(melonbooks)
            for info_dic in melonbooks:
                n_type_id = str(info_dic['type_id'])
                if n_type_id == type_id:
                    response = insert_doujinshi(info_dic)
                    if response == -1:
                        flash("传值错误")
                        break
                    elif response == -2:
                        flash("提交失败")
                        break
    dlsite = read_dlsite()
    melonbooks = read_melonbooks()

    info_list = []

    dlsite_logo = url_for('static', filename='img/site/logo-dlsite.png')
    melonbooks_logo = url_for('static', filename='img/site/logo-melonbooks.png')
    # for
    manga = []
    illustration = []
    novel = []

    for info_dic in dlsite:
        type_id = info_dic['type_id']
        if type_id == 1:
            manga.append(info_dic)
        elif type_id == 2:
            illustration.append(info_dic)
        elif type_id == 3:
            novel.append(info_dic)

    manga = not_exist(manga)
    illustration = not_exist(illustration)
    novel = not_exist(novel)
    new_num = len(manga) + len(illustration) + len(novel)

    info_list.append(['漫画', dlsite_logo, len(manga), 1, 1])
    info_list.append(['画册', dlsite_logo, len(illustration), 2, 1])
    info_list.append(['同人文', dlsite_logo, len(novel), 3, 1])

    manga = []
    illustration = []
    novel = []

    for info_dic in melonbooks:
        type_id = info_dic['type_id']
        if type_id == 1:
            manga.append(info_dic)
        elif type_id == 2:
            illustration.append(info_dic)
        elif type_id == 3:
            novel.append(info_dic)

    manga = not_exist(manga)
    illustration = not_exist(illustration)
    novel = not_exist(novel)
    new_num += len(manga) + len(illustration) + len(novel)

    info_list.append(['漫画', melonbooks_logo, len(manga), 1, 2])
    info_list.append(['画册', melonbooks_logo, len(illustration), 2, 2])
    info_list.append(['同人文', melonbooks_logo, len(novel), 3, 2])

    url_dic = init_dic()
    url_dic.update({
        'dlsite': len(dlsite),
        'melonbooks': len(melonbooks),
        'new_num': new_num,
        'info_list': info_list,
    })
    return render_template('batch_import.html', **url_dic)


@bp.route('/batch_url')
def batch_url():
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for("user.route"))

    dlsite = read_dlsite()
    for info_dic in dlsite:
        doujinshi_name = info_dic['doujinshi_name']
        doujinshi_id = get_doujinshi_id(doujinshi_name)
        doujinshi_url = info_dic['doujinshi_url']
        platform_id = info_dic['platform_id']
        create_doujinshi_url(doujinshi_id, platform_id, doujinshi_url)
    melonbooks = read_melonbooks()
    for info_dic in melonbooks:
        doujinshi_name = info_dic['doujinshi_name']
        doujinshi_id = get_doujinshi_id(doujinshi_name)
        doujinshi_url = info_dic['doujinshi_url']
        platform_id = info_dic['platform_id']
        create_doujinshi_url(doujinshi_id, platform_id, doujinshi_url)
    flash("处理完毕")
    return redirect(url_for('admin.index'))
