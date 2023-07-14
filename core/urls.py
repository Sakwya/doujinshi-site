from flask import url_for, session
from core.fetch import get_username


def init_dic(title="未命名的页面"):
    dev = False
    user_id = session.get('user_id')

    if user_id == 0:
        dev = True
    if user_id is None:
        username = "未登录"
    else:
        username = get_username(user_id)
    url_dic = {
        'title': title,
        'index': url_for('index'),
        'account': session.get('account'),
        'username': username,
        'doujinshi': url_for('doujinshi.home'),
        'search': url_for('doujinshi.search'),
        # 用户登录
        'login': url_for('user.login'),
        'signup': url_for('user.signup'),
        # 首页分类
        'manga': url_for('manga'),
        'illustration': url_for('illustration'),
        'novel': url_for('novel'),
        # tag页面
        'tag': url_for('tag.tags'),
        # 同人志页面
        'doujinshi_manga': url_for('doujinshi.manga'),
        'doujinshi_illustration': url_for('doujinshi.illustration'),
        'doujinshi_novel': url_for('doujinshi.novel'),
        # 用户功能
        'user': url_for('user.route'),
        'collection': url_for('user.collection'),
        'upload': url_for('upload.upload'),
        'logout': url_for('user.login') + "?logout=1",
        # 个人设置
        'configure': url_for('user.configure'),
        'reset': url_for('user.reset'),
        # 管理员功能
        'dev': dev,
        'admin': url_for('admin.index'),
        'review': url_for('admin.review'),
        'recover': url_for('admin.recover'),
        "batch_import": url_for("admin.batch_import"),
        "batch_url": url_for("admin.batch_url"),
    }
    return url_dic
