import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
from core.urls import init_dic
from core.fetch import get_username, get_user_info
from datetime import datetime

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
    result = db.execute(
        "SELECT doujinshi_name,author_id,type_id,uploader_id,doujinshi_cover,market,pages FROM doujinshi "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    ).fetchone()
    if result is None:
        flash("找不到该页面")
        return redirect(url_for('doujinshi.home'))
    doujinshi_name, author_id, type_id, uploader_id, doujinshi_cover, market, pages = result

    if author_id is None:
        author_name = "未知"
        author_page = ""
    else:
        author_name = db.execute(
            "SELECT author_name FROM author WHERE author_id = ?",
            (author_id,)
        ).fetchone()[0]
        author_page = "1"

    type_name = ["未知", "漫画", "画册", "同人文", "刊物"][type_id]

    if doujinshi_cover is None:
        doujinshi_cover = url_for('static', filename="no_cover.jpg")
    else:
        doujinshi_cover = url_for('static', filename="img/cover/" + doujinshi_cover)
    if pages is None:
        pages = "未知"

    head_img = db.execute(
        "SELECT head_img FROM user WHERE user_id= ?",
        (user_id,)
    ).fetchone()
    print(user_id, head_img, head_img)
    if head_img[0] is None:
        head_img = url_for('static', filename="img/user/no_head.png")
    else:
        head_img = url_for('static', filename="img/user/head_img/" + head_img[0])
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
        print(comment)
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

        'collected': collected,
        'collect': url_for('doujinshi.collect', doujinshi_id=doujinshi_id),
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
