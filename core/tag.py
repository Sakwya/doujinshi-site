import math

from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash

from core.db import get_db
from core.urls import init_dic
from core.fetch import get_tag, getAll_by_tag
import random

bp = Blueprint('tag', __name__, url_prefix='/tag')


@bp.route('/<tag_id>')
def index(tag_id):
    if session.get('user_id') is None:
        flash("请先进行登录")
        return redirect(url_for('user.login'))

    db = get_db()
    tag_name = db.execute(
        "SELECT tag_name FROM tag "
        "WHERE tag_id =? "
        "LIMIT 1",
        (tag_id,)
    ).fetchone()
    if tag_name is None:
        flash("错误的页面")
        redirect(url_for('tag.tags'))
    else:
        tag_name = tag_name[0]
    url_dic = init_dic(tag_name + "的作品")
    url_dic.update({
        "tag_name": tag_name,
        "doujinshi_list": getAll_by_tag(tag_name),
    })
    return render_template('tag.html', **url_dic)


@bp.route('index/')
@bp.route('index/<page>')
def tags(page=1):
    if session.get('user_id') is None:
        flash("请先进行登录")
        return redirect(url_for('user.login'))

    db = get_db()
    try:
        page = int(page)
    except ValueError:
        flash("错误的页码")
        return redirect(url_for('tag.tags'))
    tag_num = db.execute(
        "SELECT COUNT(*) FROM tag"
    ).fetchone()[0]

    page_num = math.ceil(tag_num / 30)
    if page > page_num:
        return redirect(url_for('tag.tags', page=page_num))

    tag_list = get_tag(30, (page - 1) * 30)

    url_dic = init_dic()
    url_dic.update({
        'tag_list': tag_list,
        'page': page,
        'page_num': page_num,
    })
    return render_template('tags.html', **url_dic)
