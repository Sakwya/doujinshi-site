import functools
import math
import os.path
from typing import List, Any

from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
from core.operate import remove_doujinshi, get_tag_id
from core.urls import init_dic
from core.fetch import get_username, get_user_info, get_doujinshi, getAll_like, getAll_by_uploader
from datetime import datetime

bp = Blueprint('doujinshi', __name__, url_prefix='/doujinshi')


@bp.route('/')
def home():
    return redirect(url_for('doujinshi.manga'))


@bp.route('/manga/')
@bp.route('/manga/<page>')
def manga(page=1):
    user_id = session.get('user_id')
    if user_id is None:
        flash('请先进行登陆！')
        return redirect(url_for('user.login'))
    db = get_db()
    try:
        page = int(page)
    except ValueError:
        flash("错误的页码")
        return redirect(url_for('doujinshi.manga'))
    doujinshi_num = db.execute(
        "SELECT COUNT(*) FROM manga_in_order"
    ).fetchone()[0]
    page_num = math.ceil(doujinshi_num / 30)
    if page > page_num:
        return redirect(url_for('doujinshi.manga', page=page_num))

    doujinshi_list = get_doujinshi(30, 1, (page - 1) * 30)

    url_dic = init_dic("漫画")
    url_dic.update({
        'type_id': 1,
        'doujinshi_list': doujinshi_list,
        'url': url_dic['doujinshi_manga'],
        'page': page,
        'page_num': page_num,
    })
    return render_template('doujinshi.html', **url_dic)


@bp.route('/illustration/')
@bp.route('/illustration/<page>')
def illustration(page=1):
    user_id = session.get('user_id')
    if user_id is None:
        flash('请先进行登陆！')
        return redirect(url_for('user.login'))
    db = get_db()
    try:
        page = int(page)
    except ValueError:
        flash("错误的页码")
        return redirect(url_for('doujinshi.illustration'))
    doujinshi_num = db.execute(
        "SELECT COUNT(*) FROM illustration_in_order"
    ).fetchone()[0]
    page_num = math.ceil(doujinshi_num / 30)
    if page > page_num:
        return redirect(url_for('doujinshi.illustration', page=page_num))

    doujinshi_list = get_doujinshi(30, 2, (page - 1) * 30)

    url_dic = init_dic("画集")
    url_dic.update({
        'type_id': 2,
        'doujinshi_list': doujinshi_list,
        'url': url_dic['doujinshi_illustration'],
        'page': page,
        'page_num': page_num,
    })
    return render_template('doujinshi.html', **url_dic)


@bp.route('/novel/')
@bp.route('/novel/<page>')
def novel(page=1):
    user_id = session.get('user_id')
    if user_id is None:
        flash('请先进行登陆！')
        return redirect(url_for('user.login'))
    db = get_db()
    try:
        page = int(page)
    except ValueError:
        flash("错误的页码")
        return redirect(url_for('doujinshi.novel'))
    doujinshi_num = db.execute(
        "SELECT COUNT(*) FROM novel_in_order"
    ).fetchone()[0]
    page_num = math.ceil(doujinshi_num / 30)
    if page > page_num:
        return redirect(url_for('doujinshi.novel', page=page_num))

    doujinshi_list = get_doujinshi(30, 3, (page - 1) * 30)

    url_dic = init_dic("小说")
    url_dic.update({
        'type_id': 3,
        'doujinshi_list': doujinshi_list,
        'url': url_dic['doujinshi_novel'],
        'page': page,
        'page_num': page_num,
    })
    return render_template('doujinshi.html', **url_dic)


@bp.route('/<doujinshi_id>', methods=('GET', 'POST'))
def index(doujinshi_id):
    user_id = session.get('user_id')
    if user_id is None:
        flash('请先进行登陆！')
        return redirect(url_for('user.login'))
    db = get_db()

    if request.method == "POST":
        comment = request.form['comment'].replace('\r\n', "&enter;")
        db.execute(
            "INSERT INTO comment (doujinshi_id,user_id,comment,date) "
            "VALUES(?,?,?,date('now')) ",
            (doujinshi_id, user_id, comment)
        )
        db.commit()
        return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))

    info = db.execute(
        "SELECT doujinshi_name,author_id,type_id,uploader_id,doujinshi_cover,market,pages FROM doujinshi "
        "WHERE doujinshi_id = ? "
        "LIMIT 1",
        (doujinshi_id,)
    ).fetchone()
    if info is None:
        flash("找不到该页面")
        return redirect(url_for('doujinshi.home'))
    doujinshi_name, author_id, type_id, uploader_id, doujinshi_cover, market, pages = info

    if author_id is None:
        author_name = "未知"
        author_page = ""
    else:
        author_name = db.execute(
            "SELECT author_name FROM author WHERE author_id = ?",
            (author_id,)
        ).fetchone()[0]
        author_page = url_for('author.page', author_id=author_id)

    type_name = ["未知", "漫画", "画册", "同人文", "刊物"][type_id]

    if doujinshi_cover is None or doujinshi_cover.find('.') == -1:
        doujinshi_cover = url_for('static', filename="no_cover.jpg")
    else:
        doujinshi_cover = url_for('static', filename="img/cover/" + doujinshi_cover)
    if pages is None:
        pages = "未知"

    head_img = get_user_info(user_id)[1]
    collected = db.execute(
        "SELECT * FROM collection "
        "WHERE user_id = ? AND doujinshi_id = ?",
        (user_id, doujinshi_id)
    ).fetchone()
    if collected is None:
        collected = "False"
    else:
        collected = "True"
    url_dic = init_dic(doujinshi_name)

    tag_list = []
    tags: list[Any] = db.execute(
        "SELECT tag_id,tag_name FROM tag "
        "WHERE tag_id in "
        "(SELECT tag_id FROM doujinshi_tag "
        "WHERE doujinshi_id = ?)",
        (doujinshi_id,)
    ).fetchall()
    for tag in tags:
        tag_list.append([url_for('tag.index', tag_id=tag[0]), tag[1], tag[0]])
    url_list = []
    urls = db.execute(
        "SELECT platform_id,doujinshi_url FROM doujinshi_url "
        "WHERE doujinshi_id =?",
        (doujinshi_id,)
    ).fetchall()

    dlsite_logo = url_for('static', filename='img/site/logo-dlsite.png')
    melonbooks_logo = url_for('static', filename='img/site/logo-melonbooks.png')
    toranoana_logo = url_for('static', filename='img/site/logo-toranoana.svg')

    for info in urls:
        url_list.append([['',dlsite_logo,melonbooks_logo,toranoana_logo][info[0]], info[1]])

    info_list = db.execute(
        "SELECT user_id,comment,date FROM comment "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    ).fetchall()
    comment_list = []
    for info in info_list:
        user_info = get_user_info(info[0])
        comment = info[1].replace("&enter;", "\n")
        comment_list.append(
            [user_info[0], user_info[1], url_for("user.index", user_id=info[0]), comment, info[2]])

    url_dic.update({
        'doujinshi_id': doujinshi_id,
        'doujinshi_name': doujinshi_name,
        'author_name': author_name,
        'author_page': author_page,
        'type': type_name,
        'doujinshi_cover': doujinshi_cover,
        'market': market,
        'pages': pages,
        'uploader_name': get_username(uploader_id),
        'uploader_page': url_for('doujinshi.uploader', uploader_id=uploader_id),
        'tag_list': tag_list,
        'url_list': url_list,

        'collected': collected,
        'collect': url_for('doujinshi.collect', doujinshi_id=doujinshi_id),
        'remove': url_for('doujinshi.remove', doujinshi_id=doujinshi_id),
        'edit': url_for('doujinshi.edit', doujinshi_id=doujinshi_id),

        'head_img': head_img,
        'comment_list': comment_list,
    })

    return render_template("artwork.html", **url_dic)


@bp.route('/<doujinshi_id>/collect', methods=('GET', 'POST'))
def collect(doujinshi_id):
    if request.method == 'GET':
        return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.route'))
    db = get_db()
    info = db.execute(
        "SELECT * FROM collection "
        "WHERE user_id = ? AND doujinshi_id = ?",
        (user_id, doujinshi_id)
    ).fetchone()
    if info is None:
        try:
            db.execute(
                "INSERT INTO collection (user_id,doujinshi_id) "
                "VALUES (?,?)",
                (user_id, doujinshi_id)
            )
            db.commit()
            return "True"
        except ValueError:
            return "False"
    else:
        try:
            db.execute(
                "DELETE FROM collection "
                "WHERE user_id = ? AND doujinshi_id =?",
                (user_id, doujinshi_id)
            )
            db.commit()
            return "False"
        except ValueError:
            return "True"


@bp.route('/<doujinshi_id>/remove', methods=('GET', 'POST'))
def remove(doujinshi_id):
    if request.method == 'GET':
        return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))
    user_id = session.get('user_id')
    if user_id != 0:
        return redirect(url_for('user.route'))

    result = remove_doujinshi(doujinshi_id)
    if result == -2:
        return "ERROR ID"
    if result == -1:
        return "FAIL"
    if result == 0:
        return "SUCCESS"


@bp.route('/<doujinshi_id>/edit', methods=('GET', 'POST'))
def edit(doujinshi_id):
    if request.method == 'GET':
        return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.route'))

    db = get_db()
    info = db.execute(
        "SELECT * FROM doujinshi "
        "WHERE doujinshi_id = ? "
        "LIMIT 1",
        (doujinshi_id,)
    ).fetchone()
    if info is None:
        flash("错误的ID")
        return redirect(url_for('doujinshi.home'))

    app = request.form['append']
    rem = request.form['remove']
    if app != "":
        app = app.split("#")
    else:
        app = []
    if rem != "":
        rem = rem.split('/')
    else:
        rem = []
    while "" in app:
        app.remove("")
    while "" in rem:
        rem.remove("")
    try:
        rem = list(map(int, rem))
    except ValueError:
        flash("操作错误")
        return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))

    for tag_id in rem:
        if db.execute(
                "SELECT * FROM doujinshi_tag "
                "WHERE doujinshi_id = ? AND tag_id = ? "
                "LIMIT 1",
                (doujinshi_id, tag_id)
        ).fetchone() is None:
            flash("删除操作错误")
            return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))

        try:
            db.execute(
                "INSERT INTO tag_op_record (doujinshi_id,tag_id,editor_id,op_type) "
                "VALUES (?,?,?,\"DELETE\")",
                (doujinshi_id, tag_id, user_id)
            )
            db.commit()
            db.execute(
                "DELETE FROM doujinshi_tag "
                "WHERE doujinshi_id = ? AND tag_id = ?",
                (doujinshi_id, tag_id)
            )
            db.commit()
        except ValueError:
            flash("删除操作错误")
            return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))

    for tag_name in app:
        tag_id = get_tag_id(tag_name)
        try:
            db.execute(
                "INSERT INTO tag_op_record (doujinshi_id,tag_id,editor_id,op_type) "
                "VALUES (?,?,?,\"INSERT\")",
                (doujinshi_id, tag_id, user_id)
            )
            db.commit()
            db.execute(
                "INSERT INTO doujinshi_tag (doujinshi_id,tag_id) "
                "VALUES (?, ?)",
                (doujinshi_id, tag_id)
            )
            db.commit()
        except ValueError:
            flash("插入操作错误")
            return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))

    flash("操作成功")
    return redirect(url_for('doujinshi.index', doujinshi_id=doujinshi_id))


@bp.route('/search', methods=['GET', 'POST'])
def search():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.route'))
    db = get_db()
    key = request.args.get('key')
    type_id = request.args.get('type')
    if key is None:
        flash("先填写关键词,再搜索")
        return redirect(url_for('manga'))

    filepath = os.path.join(os.getcwd(), "core\\static\\" + str(user_id) + ".temp")
    if os.path.exists(filepath):
        f = open(filepath, mode='r', encoding='utf-8')
        date = f.readline()[:-1]
        f.close()
        try:
            date = (datetime.now() - datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
            print(date.days, date.seconds)
            if date.seconds > 2:
                pass
            else:
                flash("搜索过于频繁,请等待后重试")
                return redirect(url_for('manga'))
        except ValueError:
            pass
    f = open(filepath, mode='w', encoding='utf-8')
    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n' + key)
    f.close()
    doujinshi_list = getAll_like(key)

    url_dic = init_dic(key + "的搜索结果")
    url_dic.update({
        'key': key,
        'num': len(doujinshi_list),
        'doujinshi_list': doujinshi_list[-30:],
    })
    return render_template("search.html", **url_dic)


@bp.route('/uploader/<uploader_id>')
def uploader(uploader_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.route'))
    uploader_name = get_username(uploader_id)
    if uploader_name == -1:
        flash("错误的值")
        return redirect(url_for('user.route'))
    url_dic = init_dic("上传者:" + uploader_name)
    doujinshi_list = getAll_by_uploader(uploader_id)
    url_dic.update({
        'uploader_page': url_for('user.index', user_id=uploader_id),
        'uploader_name': uploader_name,
        'doujinshi_list': doujinshi_list,
    })
    return render_template("uploader.html", **url_dic)
