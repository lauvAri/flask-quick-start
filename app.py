# 导入Flask类
from flask import Flask, request, url_for
from werkzeug.utils import secure_filename
'''
request 请求对象
'''

# 创建Flask类的实例
app = Flask(__name__)

'''
route()装饰器告诉Flask触发函数的URL
即把函数绑定到URL
'''
@app.route('/')
def hello_world():
    return "Hello, World!"

'''
<>可以定义动态路由
'''
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {subpath}'

'''
定义路由时，可以使用methods参数指定HTTP方法类型
缺省HTTP方法时，一个路由只回应GET请求
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do the post'
    else:
        return 'show the login form'

'''
要获取?key=value时
使用request.args.get('key','')
'''
@app.route('/get-args')
def get_args():
    value = request.args.get('key', '')
    if value:
        return f'key is {value}'
    else:
        return 'missing the key'

'''
request对象的files属性可以访问上传的文件

curl测试：
echo "This is a test file." > test.txt
curl -X POST -F "the_file=@test.txt" http://127.0.0.1:5000/upload
curl http://127.0.0.1:5000/static/uploads/test.txt
'''
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('static/uploads/'+secure_filename(f.filename))
        return 'http://127.0.0.1:5000/static/uploads/'+secure_filename(f.filename)
    else:
        return 'please use POST'
    
'''
JSON api
'''

class User:
    def __init__(self, username, theme, image):
        self.username = username
        self.theme = theme
        self.image = image
    # 返回一个用户的信息
    def __repr__(self):
        return (
            f'User(username={self.username}, '
            f'theme={self.theme}, '
            f'image={self.image}'
        )
    
@app.route('/me')
def me():
    user = User('Jack', 'Dark', 'a.png')
    app.logger.debug(f'create the user: {user.__repr__()}')
    return {
      "username":user.username,
      "theme":user.theme,
      "image": f'http://127.0.0.1:5000/static/images/{user.image}'
    }

# 使用蓝图有利于模块化
from . import users
app.register_blueprint(users.bp)