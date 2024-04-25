import flask
from nmapfun import *
from flask import request
from flask import Flask

app = Flask(__name__,
            static_url_path='/static',  # 静态文件路径
            static_folder='static',
            template_folder='templates'  # 模板文件
            )


@app.route('/')
def welcome():
    return flask.render_template('welcome.html')


@app.route('/menu')
def menu():
    return flask.render_template('menu.html')


@app.route('/menu/nmapfun', methods=['GET', 'POST'])
def nmapfun():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'query_myself':
            user_ip = request.remote_addr
            result = query(user_ip)
            return flask.render_template('nmapfun.html', result=result)
        elif action == 'query_other_user':
            ip = request.form.get('ip')
            result = query(ip)
            return flask.render_template('nmapfun.html', result=result)
        elif action == 'query_network':
            ip = request.form.get('network')
            result = query(ip)
            return flask.render_template('nmapfun.html', result=result)
    # 默认情况下渲染菜单页面模板
    return flask.render_template('nmapfun.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
