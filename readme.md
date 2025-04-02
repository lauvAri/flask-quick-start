内容来自：https://flask.github.net.cn/
# 1. 安装

创建虚拟环境也可以使用conda，根据自己喜好选择即可

## 创建虚拟环境
```
python -m venv venv
```
执行后生成venv文件夹

## 激活虚拟环境
在开始工作前，先要激活相应的虚拟环境
```
venv\Scripts\activate
```

## 安装flask
```
pip install Flask
```

# 2. 启动服务器

在CMD中
```
set FLASK_APP=app.py
flask run
```

在PowerShell中
```
$env:FLASK_APP = "app.py"
flask run --reload
```

`--reload`参数表示开启热重载hmr, 更多参数参考 flask run --help

```
* Running on http://127.0.0.1:5000
```
