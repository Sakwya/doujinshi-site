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
    if user is None:
        return -1
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


def get_collection(num, user_id, type_id=0):
    db = get_db()
    if type_id == 0:
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
            (str(type_id), user_id, num)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None or piece[2].find('.') == -1:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def getAll_like(key):
    db = get_db()
    info = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id "
        "FROM doujinshi "
        "WHERE doujinshi_name LIKE ? ",
        ('%'+key+'%',)
    ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None or piece[2].find('.') == -1:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list

def getAll_collection(user_id, type_id=0):
    db = get_db()
    if type_id == 0:
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
            (str(type_id), user_id)
        ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None or piece[2].find('.') == -1:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_by_author(author_id, num=18):
    db = get_db()
    info = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
        "WHERE author_id =? "
        "LIMIT ?",
        (author_id, num)
    ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None or piece[2].find('.') == -1:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def getAll_by_author(author_id):
    db = get_db()
    info = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
        "WHERE author_id =?",
        (author_id,)
    ).fetchall()
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None or piece[2].find('.') == -1:
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
        if piece[2] is None or piece[2].find('.') == -1:
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
        if piece[2] is None or piece[2].find('.') == -1:
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
        if piece[2] is None or piece[2].find('.') == -1:
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
        if piece[2] is None or piece[2].find('.') == -1:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_doujinshi(num=30, type_id=0, start=0):
    db = get_db()
    if start == 0:
        if type_id == 0:
            info = db.execute(
                "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi_in_order "
                "LIMIT ?",
                (num,)
            ).fetchall()
        else:
            info = db.execute(
                "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi_in_order "
                "WHERE type_id = ? "
                "LIMIT ?",
                (type_id, num)
            ).fetchall()
    else:
        if type_id == 0:
            info = db.execute(
                "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi_in_order "
                "WHERE no>? AND no<=?"
                "LIMIT ?",
                (start, start + num, num)
            ).fetchall()
        elif type_id == 1:
            info = db.execute(
                "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM manga_in_order "
                "WHERE no>? AND no<=? AND type_id = ?"
                "LIMIT ?",
                (start, start + num, 1, num)
            ).fetchall()
        elif type_id == 2:
            info = db.execute(
                "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM illustration_in_order "
                "WHERE no>? AND no<=? AND type_id = ?"
                "LIMIT ?",
                (start, start + num, 2, num)
            ).fetchall()
        elif type_id == 3:
            info = db.execute(
                "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM novel_in_order "
                "WHERE no>? AND no<=? AND type_id = ?"
                "LIMIT ?",
                (start, start + num, 3, num)
            ).fetchall()
        else:
            return -1
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None or piece[2].find('.') == -1:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        else:
            pieces.append(url_for('static', filename='img/cover/' + piece[2]))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_tag(num=30, start=0):
    db = get_db()
    if start == 0:
        info = db.execute(
            "SELECT no, tag_id,tag_name,num FROM tag_in_order "
            "LIMIT ?",
            (num,)
        ).fetchall()
    else:
        info = db.execute(
            "SELECT no, tag_id,tag_name,num FROM tag_in_order "
            "WHERE no>? AND no<=?"
            "LIMIT ?",
            (start, start + num, num)
        ).fetchall()
    info_list = []
    for piece in info:
        info_list.append([piece[0], url_for('tag.index', tag_id=piece[1]), piece[2], piece[3]])
    return info_list


def get_by_id(doujinshi_id):
    db = get_db()
    piece = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    ).fetchone()

    pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
    if piece[2] is None or piece[2].find('.') == -1:
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
    info_list = [[], [], [], []]
    for piece in info:
        info_list[piece[1]].append(str(piece[0]))

    manga = _random18(info_list[1])
    illustration = _random18(info_list[2])
    novel = _random18(info_list[3])

    info_list = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n', "@manga\n"]
    for info in manga:
        info_list.append(info + '\n')
    info_list.append("@illustration\n")
    for info in illustration:
        info_list.append(info + '\n')
    info_list.append("@novel\n")
    for info in novel:
        info_list.append(info + '\n')
    info_list.append("@end\n")

    tag_list = db.execute(
        "SELECT tag_id,tag_name FROM tag"
    ).fetchall()
    tag_list = _random18(tag_list)[:4]
    for tag in tag_list:
        info_list.append('@tag\n')
        info_list.append(tag[1] + '\n')
        info_list.append(url_for('tag.index', tag_id=tag[0]) + '\n')
        info = db.execute(
            "SELECT doujinshi_id FROM doujinshi_tag "
            "WHERE tag_id = ? "
            "LIMIT 6",
            (tag[0],)
        ).fetchall()
        info = _random18(info)
        if len(info) > 6:
            info = info[:6]
        for piece in info:
            info_list.append(str(piece[0]) + '\n')
        info_list.append('@end\n')

    filepath = os.path.join(os.getcwd(), "core\\static\\random.temp")
    f = open(filepath, 'w', encoding='utf-8')
    f.writelines(info_list)
    f.close()


def get_random(type_id, num=18):
    filepath = os.path.join(os.getcwd(), "core\\static\\random.temp")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            date = f.readline()[:-1]
            f.close()
            try:
                date = (datetime.datetime.now() - datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
                if date.days > 0 or date.seconds > 10:
                    set_random()
            except ValueError:
                set_random()
    else:
        set_random()
    with open(filepath, 'r', encoding='utf-8') as f:
        info_list = f.readlines()
        f.close()
    info_list.pop(0)
    manga = info_list.index("@manga\n")
    illustration = info_list.index("@illustration\n")
    novel = info_list.index("@novel\n")
    end = info_list.index("@end\n")
    manga = info_list[manga + 1:illustration]
    illustration = info_list[illustration + 1:novel]
    novel = info_list[novel + 1:end]

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
    return -1


def get_random_by_tag(num=6):
    if num > 6:
        return -1
    filepath = os.path.join(os.getcwd(), "core\\static\\random.temp")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            date = f.readline()[:-1]
            f.close()
            try:
                date = (datetime.datetime.now() - datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
                if date.days > 0 or date.seconds > 10:
                    set_random()
            except ValueError:
                set_random()
    else:
        set_random()
    with open(filepath, 'r', encoding='utf-8') as f:
        info_list = f.readlines()
        f.close()
    info_list.pop(0)

    doujinshi_tag_list = []
    while "@tag\n" in info_list:
        tag_start = info_list.index("@tag\n")
        info_list = info_list[tag_start + 1:]
        tag_name = info_list.pop(0)[:-1]
        tag_page = info_list.pop(0)[:-1]
        tag_end = info_list.index("@end\n")
        doujinshi_id_list = info_list[:tag_end]
        doujinshi_list = []
        for doujinshi_id in doujinshi_id_list:
            doujinshi_list.append(get_by_id(doujinshi_id[:-1]))
        doujinshi_tag_list.append([[tag_page, tag_name], doujinshi_list[:num]])
    return doujinshi_tag_list


def get_random_tag(num=18):
    db = get_db()
    tags = db.execute(
        "SELECT tag_id,tag_name FROM tag"
    ).fetchall()
    tags = _random18(tags)
    tag_list = []
    for tag in tags:
        tag_list.append([url_for('tag.index', tag_id=tag[0]), tag[1]])
    return tag_list
