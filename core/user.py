import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
from core.urls import init_dic

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # POST访问方式，进入表单与数据库的注册后台逻辑
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        # 后端验证username、password是否缺失
        if not username:
            error = '用户名不能为空！'
        elif not password:
            error = '密码不能为空！'

        # 通过验证后，查询数据库，无错误时写入数据，完成注册。有错误反馈。
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (user_name, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f'用户 {username} 已经注册过！'
            else:
                flash('恭喜你注册成功~☆')
                return redirect(url_for('user.login'))

        # 页面闪现错误提示
        flash(error)

    # GET访问方式，直接返回注册页面
    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # POST访问方式，进入表单与数据库的注册后台逻辑
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE user_name= ?",
            (username,)
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
            session['user_name'] = username
            flash('登陆成功')
            if username == 'manager':
                return redirect(url_for('admin.index'))
            return redirect(url_for('user.route'))

        # 页面闪现错误提示
        flash(error)

    if request.args.get('logout') == '1':
        session.clear()
        flash("退出登录成功！")

    # GET访问方式，直接返回登陆页面
    return render_template('login.html')


@bp.route('/')
def route():
    user_id = session.get('user_id')
    if user_id == 'none':
        return redirect(url_for('user.login'))
    return redirect(url_for('user.index', user_id=user_id))


@bp.route('/<user_id>')
def index(user_id):
    if str(session.get('user_id')) != user_id:
        return redirect(url_for('user.login'))

    db = get_db()
    error = None

    user = db.execute(
        "SELECT * FROM user WHERE user_id= ?",
        (user_id,)
    ).fetchone()
    if user is None:
        session.clear()
        error = '用户不存在'
        flash(error)
        return render_template('login.html')

    results = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover FROM doujinshi "
        "WHERE doujinshi_id in "
        "(SELECT doujinshi_id from usercollection where user_id =?)",
        (user_id,)
    ).fetchall()
    collections = []
    for result in results:
        collection = [result[1], url_for('doujinshi.index', doujinshi_id=result[0])]
        if result[2] is None:
            collection.append(url_for('static', filename='no_cover.jpg'))
        collections.append(collection)

    results = db.execute(
        "SELECT doujinshi_id,doujinshi_name,doujinshi_cover FROM doujinshi "
        "WHERE user_id=? ",
        (user_id,)
    ).fetchall()
    artworks = []
    for result in results:
        artwork = [result[1], url_for('doujinshi.index', doujinshi_id=result[0])]
        if result[2] is None:
            artwork.append(url_for('static', filename='no_cover.jpg'))
        artworks.append(artwork)

    unconfirmed = len(db.execute(
        "SELECT * FROM unconfirmed "
        "WHERE user_id=? ",
        (user_id,)
    ).fetchall())
    url_dic = init_dic(user)
    url_dic.update({
        'collections': collections,
        'artworks': artworks,
        'unconfirmed': unconfirmed,
    })

    # GET访问方式，直接返回登陆页面
    return render_template('user.html', **url_dic)
