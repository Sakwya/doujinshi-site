import os
from flask import Flask,render_template


def create_app(test_config=None):

    app = Flask(__name__,
            static_url_path="/static",  # 访问静态资源的url前缀，默认值是static
            static_folder="static",  # 设置静态文件的目录，默认值是static
            template_folder="templates"  # 设置模板文件的目录，默认值是templates
            )

    # 2.设置SECRET_KEY和数据库实例路径
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'doujinshi.sqlite'),
    )

    # 3.根据提供的参数启动特定模式，如开发模式、测试模式、生产模式等。
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 4.创建数据库实例文件夹，没有文件夹则建立，若已存在则报错，但pass
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 5.创建一个路由，验证工厂函数是否正常
    @app.route('/')
    @app.route('/home')
    def index():
        return render_template('index.html')

    from core import db
    db.init_app(app)

    from . import doujinshi,user,admin,upload
    app.register_blueprint(doujinshi.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(upload.bp)

    # 6.返回框架实例：一个可调用框架对象
    return app

