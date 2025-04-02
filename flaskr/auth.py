import functools

from flask import (
    Blueprint, flash, g, 
    redirect, render_template, 
    request, session, url_for
)

from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from flaskr.db import get_db

# Blueprint 是一种组织一组相关视图及其他代码的方式
# 把视图和其他代码注册到蓝图中，然后再工厂函数中把蓝图注册到应用中

'''
创建了一个名称为 'auth' 的 Blueprint 。
和应用对象一样， 蓝图需要知道是在哪里定义的，
因此把 __name__ 作为函数的第二个参数。 
url_prefix 会添加到所有与该蓝图关联的 URL 前面。
'''

bp = Blueprint('auth', __name__, url_prefix='/auth')


'''
视图是一个应用对请求进行响应的函数。 
Flask 通过模型把进来的请求 URL 匹配到 对应的处理视图(函数)。

@bp.route 关联了 URL /register 和 register 视图函数
request.form 是一个特殊类型的 dict(字典， 类似Java中的Map) ，其映射了提交表单的键和值。
'''
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is not required.'
        elif db.execute(
            # ? 占位符
            # 使用占位符的 好处是会自动帮你转义输入值，以抵御 SQL 注入攻击 。
            'SELECT id FROM user WHERE username = ?',
            # 元组 
            (username,)    
        ).fetchone() is not None:
            error = f'User {username} is already registered.'
        
        if error is None:
            db.execute(
               'INSERT INTO user (username, password) VALUES(?, ?)',
               (username, generate_password_hash(password))
               # 不能把密码明文 储存在数据库中。
               # 相代替的，使用 generate_password_hash() 生成安全的哈希值并储存 到数据库中。
            )
            db.commit()
            #  url_for() 根据登录视图(函数)的名称生成相应的 URL 。
            return redirect(url_for('auth.login'))
        
        flash(error) #  flash() 用于储存在渲染模块时可以调用的信息。
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            # session 是一个 dict ，它用于储存横跨请求的值。
            # 当验证 成功后，用户的 id 被储存于一个新的会话中。
            # 会话数据被储存到一个 向浏览器发送的 cookie 中，
            # 在后继请求中，浏览器会返回它。
            # Flask 会安全对数据进行 签名 以防数据被篡改。
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

'''
bp.before_app_request() 注册一个 在视图函数之前运行的函数，
不论其 URL 是什么。 
load_logged_in_user 检查用户 id 是否已经储存在 session 中，
并从数据库中获取用户数据，
然后储存在 g.user 中。 
g.user 的持续时间比请求要长。 
如果没有用户 id ，或者 id 不存在，那么 g.user 将会是 None 。
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    '''
    装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。
    新的函数检查用户 是否已载入。
    如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面。
    
    参数:
    - view: 被装饰的视图函数
    
    返回:
    - wrapped_view: 包装后的视图函数，用于检查用户登录状态
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # 检查当前用户是否已登录
        if g.user is None:
            # 如果用户未登录，则重定向到登录页面
            return redirect(url_for('auth.login'))
        
        # 如果用户已登录，则继续执行原视图函数
        return view(**kwargs)
    
    return wrapped_view