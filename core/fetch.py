from flask import url_for, session, flash
import datetime, random
from core.db import get_db
import os

type_list = ["未知", "漫画", "画册", "同人文", "刊物"]


def get_username(user_id):
    db = get_db()
    user = db.execute(
        "SELECT user_name FROM user WHERE user_id= ?",
        (user_id,)
    ).fetchone()
    return user[0]


def get_user_info(user_id):
    db = get_db()
    user = db.execute(
        "SELECT user_name,head_img,email FROM user WHERE user_id= ?",
        (user_id,)
    ).fetchone()
    if user[1] is None:
        head_img = url_for('static', filename="img/user/no_head.png")
    else:
        head_img = url_for('static', filename="img/user/head_img/" + user[1])
    return user[0], head_img, user[2]


def get_collection(num, user_id, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE doujinshi_id in "
            "(SELECT doujinshi_id from collection where user_id =?) "
            "LIMIT ?",
            (user_id, num)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and doujinshi_id in "
            "(SELECT doujinshi_id from collection where user_id =?) "
            "LIMIT ?",
            (type_, user_id, num)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def getAll_collection(user_id, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE doujinshi_id in "
            "(SELECT doujinshi_id from collection where user_id =?)",
            (user_id,)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and doujinshi_id in "
            "(SELECT doujinshi_id from collection where user_id =?)",
            (type_, user_id)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_by_uploader(num, uploader_id, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE uploader_id =? "
            "LIMIT ?",
            (uploader_id, num)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and uploader_id =? "
            "LIMIT ?",
            (type_, uploader_id, num)
        ).fetchmany(num)
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def getAll_by_uploader(uploader_id, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE uploader_id =?",
            (uploader_id,)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE uploader_id =?",
            (type_, uploader_id)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_by_tag(num, tag_name, type_=0):
    db = get_db()
    tag_id = db.execute(
        "SELECT tag_id FROM tag "
        "WHERE tag_name = ? ",
        (tag_name,)
    ).fetchone()[0]
    if tag_id is None:
        flash("错误的标签名")
        return -1
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE doujinshi_id in "
            "(SELECT doujinshi_id from doujinshi_tag where tag_id =?) "
            "LIMIT ?",
            (tag_id, num)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and doujinshi_id in "
            "(SELECT doujinshi_id from doujinshi_tag where tag_id =?) "
            "LIMIT ?",
            (type_, tag_id, num)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def getAll_by_tag(tag_name, type_=0):
    db = get_db()
    tag_id = db.execute(
        "SELECT tag_id FROM tag "
        "WHERE tag_name = ?",
        (tag_name,)
    ).fetchone()[0]
    if tag_id is None:
        flash("错误的标签名")
        return -1
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE doujinshi_id in "
            "(SELECT doujinshi_id from doujinshi_tag where tag_id =?)",
            (tag_id,)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and doujinshi_id in "
            "(SELECT doujinshi_id from doujinshi_tag where tag_id =?)",
            (type_, tag_id)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_doujinshi(num, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "LIMIT ?",
            (num,)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? "
            "LIMIT ?",
            (type_, num)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_by_id(doujinshi_id):
    db = get_db()
    piece = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    ).fetchone()

    pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
    if piece[2] is None:
        pieces.append(url_for('static', filename='no_cover.jpg'))
    else:
        pieces.append(url_for('static', filename='img/cover/' + piece[2]))
    pieces.append(type_list[piece[3]])
    return pieces


def _random18(full_list):
    if len(full_list) <= 18:
        return full_list
    piece_list = []
    for i in range(18):
        index = random.randrange(len(full_list))
        piece_list.append(full_list.pop(index))
    return piece_list


def set_random():
    db = get_db()
    info = db.execute(
        "SELECT doujinshi_id,type_id FROM doujinshi"
    ).fetchall()
    info_list = [[], [], [], [], []]
    for piece in info:
        info_list[piece[1]].append(str(piece[0]))
    print(info_list)

    manga = _random18(info_list[1])
    illustration = _random18(info_list[2])
    novel = _random18(info_list[3])
    magazine = _random18(info_list[4])

    info_list = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n', "@manga\n"]
    for info in manga:
        info_list.append(info + '\n')
    info_list.append("@illustration\n")
    for info in illustration:
        info_list.append(info + '\n')
    info_list.append("@novel\n")
    for info in novel:
        info_list.append(info + '\n')
    info_list.append("@magazine\n")
    for info in magazine:
        info_list.append(info + '\n')
    info_list.append("@end\n")
    print(info_list)

    filepath = os.path.join(os.getcwd(), "core\\static\\random.temp")
    f = open(filepath, 'w')
    f.writelines(info_list)
    f.close()


def get_random(type_id, num=18):
    filepath = os.path.join(os.getcwd(), "core\\static\\random.temp")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            date = f.readline()[:-1]
            f.close()
            try:
                date = (datetime.datetime.now() - datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
                if date.days > 0 or date.seconds > 3600:
                    set_random()
            except ValueError:
                set_random()
    else:
        set_random()
    with open(filepath, 'r') as f:
        info_list = f.readlines()
        f.close()
    info_list.pop(0)
    manga = info_list.index("@manga\n")
    illustration = info_list.index("@illustration\n")
    novel = info_list.index("@novel\n")
    magazine = info_list.index("@magazine\n")
    end = info_list.index("@end\n")
    manga = info_list[manga + 1:illustration]
    illustration = info_list[illustration + 1:novel]
    novel = info_list[novel + 1:magazine]
    magazine = info_list[magazine + 1:end]

    if type_id == 1:
        manga_list = []
        for piece in manga:
            manga_list.append(get_by_id(piece[:-1]))
        return manga_list[0:num]
    if type_id == 2:
        illustration_list = []
        for piece in illustration:
            illustration_list.append(get_by_id(piece[:-1]))
        return illustration_list[0:num]
    if type_id == 3:
        novel_list = []
        for piece in novel:
            novel_list.append(get_by_id(piece[:-1]))
        return novel_list[0:num]
    if type_id == 4:
        magazine_list = []
        for piece in magazine:
            magazine_list.append(get_by_id(piece[:-1]))
        return magazine_list[0:num]
    return -1
