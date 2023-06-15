from flask import url_for, session


def init_dic(title="未命名的页面"):
    dev = False
    if session.get('user_id') == 0:
        dev = True
    url_dic = {
        'title': title,
        'index': url_for('index'),
        'username': session.get('user_name'),
        # 用户登录
        'login': url_for('user.login'),
        'signup': url_for('user.signup'),
        # 首页分类
        'manga': url_for('manga'),
        'illustration': url_for('illustration'),
        'novel': url_for('novel'),
        'magazine': url_for('magazine'),
        # 用户功能
        'user': url_for('user.route'),
        'doujinshi': url_for('doujinshi.home'),
        'upload': url_for('upload.upload'),
        'logout': url_for('user.login')+"?logout=1",
        # 个人设置
        'configure': url_for('user.configure'),
        'reset':url_for('user.reset'),
        # 管理员功能
        'dev': dev,
        'admin': url_for('admin.index')
    }
    return url_dic
