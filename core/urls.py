from flask import url_for


def init_dic(title):
    url_dic = {
        'title': title,
        'index': url_for('index'),
        'doujinshi': url_for('doujinshi.home'),
        'user': url_for('user.route'),
    }
    return url_dic
