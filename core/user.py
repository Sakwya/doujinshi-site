import functools
from flask import Blueprint, request, render_template, flash, session, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash
from core.db import get_db
import smtplib
from email.mime.text import MIMEText
from email.header import Header

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

                mail_host = "smtp.163.com"  # 设置服务器
                mail_user = "sakwya_auto_sender@163.com"  # 用户名
                mail_pass = "LOUBXHDQQMSSMXSD"  # 口令

                sender = 'from@doujinshi'
                receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
                print(email, " ", username)
                # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
                message = MIMEText('恭喜你注册成功~☆', 'plain', 'utf-8')
                message['From'] = Header("管理员", 'utf-8')  # 发送者
                message['To'] = Header(username, 'utf-8')  # 接收者

                subject = '账号注册成功通知'
                message['Subject'] = Header(subject, 'utf-8')

                try:
                    smtpObj = smtplib.SMTP()
                    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
                    smtpObj.login(mail_user, mail_pass)
                    smtpObj.sendmail(sender, receivers, message.as_string())
                    print("邮件发送成功")
                except smtplib.SMTPException:
                    print("Error: 无法发送邮件")
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
            flash('登陆成功')
            if username == 'manager':
                return redirect(url_for('admin.index'))
            return redirect(url_for('user.route'))

        # 页面闪现错误提示
        flash(error)

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
        session.pop('user_id')
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

    dic = {
        'user_name': user['user_name'],
        'collections': collections,
        'artworks': artworks
    }

    # GET访问方式，直接返回登陆页面
    return render_template('user.html', **dic)