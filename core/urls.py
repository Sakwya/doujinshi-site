from flask import url_for,session


def init_dic(title):
    url_dic = {
        'title': title,
        'index': url_for('index'),
        'doujinshi': url_for('doujinshi.home'),
        'user': url_for('user.route'),
        'username': session.get('user_name'),
        'login': url_for('user.login'),
        'upload': url_for('upload.upload'),
    }
    return url_dic
