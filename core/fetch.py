from flask import url_for, session, flash
from core.db import get_db


def get_collection(num, user_id, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE doujinshi_id in "
            "(SELECT doujinshi_id from collection where user_id =?)",
            (user_id,)
        ).fetchmany(num)
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and doujinshi_id in "
            "(SELECT doujinshi_id from collection where user_id =?)",
            (type_, user_id)
        ).fetchmany(num)
    class_list = ["未知", "漫画", "插画", "小说", "杂志"]
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        pieces.append(class_list[piece[3]])
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
    type_list = ["未知", "漫画", "插画", "小说", "杂志"]
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_by_uploader(num, uploader_id, type_=0):
    db = get_db()
    if type_ == 0:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE uploader_id =?",
            (uploader_id,)
        ).fetchmany(num)
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE uploader_id =?",
            (type_, uploader_id)
        ).fetchmany(num)
    type_list = ["未知", "漫画", "插画", "小说", "杂志"]
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
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
    type_list = ["未知", "漫画", "插画", "小说", "杂志"]
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        pieces.append(type_list[piece[3]])
        info_list.append(pieces)
    return info_list


def get_by_tag(num, tag_name, type_=0):
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
        ).fetchmany(num)
    else:
        info = db.execute(
            "SELECT doujinshi_id,doujinshi_name,doujinshi_cover,type_id FROM doujinshi "
            "WHERE type_id = ? and doujinshi_id in "
            "(SELECT doujinshi_id from doujinshi_tag where tag_id =?)",
            (type_, tag_id)
        ).fetchmany(num)
    class_list = ["未知", "漫画", "插画", "小说", "杂志"]
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        pieces.append(class_list[piece[3]])
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
    class_list = ["未知", "漫画", "插画", "小说", "杂志"]
    info_list = []
    for piece in info:
        pieces = [url_for('doujinshi.index', doujinshi_id=piece[0]), piece[1]]
        if piece[2] is None:
            pieces.append(url_for('static', filename='no_cover.jpg'))
        pieces.append(class_list[piece[3]])
        info_list.append(pieces)
    return info_list
