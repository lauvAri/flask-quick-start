import os

from flask import Flask

def create_app(test_config=None):
    # 创建和配置应用
    '''
    __name__ 当前 Python 模块的名称
    instance_relative_config 配置文件是相对于 instance folder 的相对路径
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )
    
    if test_config is None:
        '''
        如果 config.py 存在的话,
        使用 config.py 中的值来重载缺省配置
        '''
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 确保 app.instance_path 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World! from flaskr'

    # 注册了一个命令行接口
    from . import db
    db.init_app(app)

    # 注册认证蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app