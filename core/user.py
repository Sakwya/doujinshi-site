import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash

from core.db import get_db
from core.urls import init_dic
from core.fetch import get_collection, get_by_uploader, get_random
import random

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<user_id>')
def index(user_id):
    # 验证登录
    if str(session.get('user_id')) != user_id:
        return redirect(url_for('user.route'))
    db = get_db()
    get_random(18)
    user = db.execute(
        "SELECT * FROM user WHERE user_id= ?",
        (user_id,)
    ).fetchone()
    if user is None:
        session.clear()
        error = '用户不存在'
        flash(error)
        return redirect(url_for('user.login'))

    if user[5] is None:
        head_img = url_for('static', filename="img/user/no_head.png")
    else:
        head_img = url_for('static', filename="img/user/head_img/" + user[5])

    collection_list = get_collection(6, user_id)
    artwork_list = get_by_uploader(6, user_id)

    unconfirmed = len(db.execute(
        "SELECT * FROM unconfirmed "
        "WHERE uploader_id=? ",
        (user_id,)
    ).fetchall())
    url_dic = init_dic(session.get('account') + '的空间')

    if user_id == '0':
        review = url_for('admin.index')
    else:
        review = None

    url_dic.update({
        'review': review,
        'email': user[4],
        'head_img': head_img,
        'collection_list': collection_list,
        'artwork_list': artwork_list,
        'unconfirmed_num': unconfirmed,
    })

    # GET访问方式，直接返回登陆页面
    return render_template('user.html', **url_dic)


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (account, password, email) VALUES (?, ?, ?)",
                (account, generate_password_hash(password), email),
            )
            db.commit()
        except db.IntegrityError:
            error = f'用户 {account} 已存在！'
        else:
            flash('恭喜你注册成功~☆')
            return redirect(url_for('user.login'))

        flash(error)
    return render_template('signup.html', **init_dic())


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # POST访问方式，进入表单与数据库的注册后台逻辑
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE account= ?",
            (account,)
        ).fetchone()

        # 后端验证用户是否能查询到，密码hash值是否能比对上
        if user is None:
            error = '用户或密码错误！'
        elif not check_password_hash(user['password'], password):
            error = '用户或密码错误！'

        # 通过验证后，设置cookie, 并跳转至首页
        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            session['account'] = account
            flash('登陆成功')
            if account == 'admin':
                return redirect(url_for('admin.index'))
            return redirect(url_for('user.route'))

        # 页面闪现错误提示
        flash(error)

    if request.args.get('logout') == '1':
        session.clear()
        flash("退出登录成功！")

    # GET访问方式，直接返回登陆页面
    return render_template('login.html', **init_dic())


@bp.route('/')
def route():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.login'))
    return redirect(url_for('user.index', user_id=user_id))


@bp.route('/configure', methods=('GET', 'POST'))
def configure():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.login'))
    if request.method == 'POST':
        db = get_db()
        user_name = request.form['username']
        try:
            db.execute(
                "UPDATE user "
                "SET user_name = ? "
                "WHERE user_id = ? ",
                (user_name, user_id),
            )
            db.commit()
        except db.IntegrityError:
            flash("昵称更改失败,请重新确认")
            return redirect(url_for('user.configure'))

        enable_img = request.form['enable_img']
        if enable_img == "f":
            flash("昵称更改成功~☆")
            return redirect(url_for('user.route'))

        head_img = request.files['head_img']
        db = get_db()
        if len(head_img.filename) == 0:
            try:
                db.execute(
                    "UPDATE user "
                    "SET head_img = null "
                    "WHERE user_id = ? ",
                    (user_id,)
                )
                db.commit()
            except db.IntegrityError:
                flash("头像更改失败,请重新确认")
                return redirect(url_for('user.configure'))
            flash("已充值为默认头像")
            return redirect(url_for("user.route"))

        ran = str(random.random())[3:8]
        filename = str(user_id) + "@" + ran + '.' + head_img.filename.split('.')[-1]
        head_img.save(
            'core/static/img/user/head_img/' + filename)
        try:
            db.execute(
                "UPDATE user "
                "SET head_img = ? "
                "WHERE user_id = ? ",
                (filename, user_id)
            )
            db.commit()
        except db.IntegrityError:
            flash("头像更改失败,请重试")
            return redirect(url_for('user.configure'))
        else:
            flash('修改成功~☆')
            return redirect(url_for('user.route'))

    return render_template('configure.html', **init_dic())


@bp.route('/reset', methods=('GET', 'POST'))
def reset():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user.login'))
    if request.method == 'POST':
        return render_template('reset.html', **init_dic())
    return render_template('reset.html', **init_dic())
