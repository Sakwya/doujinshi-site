import os
from flask import Flask, render_template, session, redirect, url_for
from core import fetch
from core.urls import init_dic


def create_app(test_config=None):
    app = Flask(__name__,
                static_url_path="/static",  # 访问静态资源的url前缀，默认值是static
                static_folder="static",  # 设置静态文件的目录，默认值是static
                template_folder="templates"  # 设置模板文件的目录，默认值是templates
                )

    # 设置SECRET_KEY和数据库实例路径
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'doujinshi.sqlite'),
    )

    # 根据提供的参数启动特定模式，如开发模式、测试模式、生产模式等。
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 4.创建数据库实例文件夹，没有文件夹则建立，若已存在则报错，但pass
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 路由
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/home')
    @app.route('/manga')
    def manga():
        user_id = session.get("user_id")
        if user_id is None:
            return redirect(url_for('user.login'))
        url_dic = init_dic()
        url_dic.update({
            'type_id': 1,
            'collection_list': fetch.get_collection(6, session.get('user_id'), 1),
            'random_list': fetch.get_random(1),
            'tag_list': fetch.get_random_tag(),
            'random_tag_list': fetch.get_random_by_tag(),
        })
        return render_template('home.html', **url_dic)

    @app.route('/illustration')
    def illustration():
        user_id = session.get("user_id")
        if user_id is None:
            return redirect(url_for('user.login'))
        url_dic = init_dic()
        url_dic.update({
            'type_id': 2,
            'collection_list': fetch.get_collection(6, session.get('user_id'), 2),
            'random_list': fetch.get_random(2),
            'tag_list': fetch.get_random_tag(),
            'random_tag_list': fetch.get_random_by_tag(),
        })
        return render_template('home.html', **url_dic)

    @app.route('/novel')
    def novel():
        user_id = session.get("user_id")
        if user_id is None:
            return redirect(url_for('user.login'))
        url_dic = init_dic()
        url_dic.update({
            'type_id': 3,
            'collection_list': fetch.get_collection(6, session.get('user_id'), 3),
            'random_list': fetch.get_random(3),
            'tag_list': fetch.get_random_tag(),
            'random_tag_list': fetch.get_random_by_tag(),
        })
        return render_template('home.html', **url_dic)


    # 数据库
    from core import db
    db.init_app(app)
    # 蓝图
    from . import doujinshi, user, admin, upload, author, tag
    app.register_blueprint(doujinshi.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(author.bp)
    app.register_blueprint(tag.bp)

    # 6.返回框架实例：一个可调用框架对象
    return app
