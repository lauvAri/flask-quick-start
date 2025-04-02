## 运行
```
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV="development"
flask run --reload
```

## 数据库设置

参照`db.py`

```
flask init-db
```
输出 Initialized the database. 说明数据库初始化成功

如果你还在运行着前一页的服务器，那么现在要么停止该服务器，要么在新的 终端中运行这个命令。如果是新的终端请记住在进行项目文件夹并激活环境， 参见 激活虚拟环境 。同时还要像前一页所述设置 FLASK_APP 和 FLASK_ENV 。

现在会有一个 flaskr.sqlite 文件出现在项目所在文件夹的 instance 文件夹 中。

## 蓝图和视图

参考`auth.py`

## 模板

模板是包含静态数据和动态数据占位符的文件。模板使用指定的数据生成最终的文档。 Flask 使用 `Jinja` 模板库来渲染模板。

模板文件会储存在 flaskr 包内的 templates 文件夹内。

任何位于 {{ 和 }} 这间的东西是一个会输出到最终文档的静态式。 {% 和 %} 之间的东西表示流程控制语句，如 if 和 for 。
