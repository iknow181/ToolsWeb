import flask
from nmapfun import *
from flask import Flask, render_template, request, redirect, session, url_for, make_response
from captcha.image import ImageCaptcha
import random
from functools import wraps

app = Flask(__name__,
            static_url_path='/static',  # 静态文件路径
            static_folder='static',
            template_folder='templates'  # 模板文件
            )
# 设置秘密密钥，用于加密会话数据
app.secret_key = 'my_secret_key'

# 假设的用户名和密码，实际情况下应该从数据库中获取
USERNAME = 'admin'
PASSWORD = 'password'


# 身份验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查用户是否已登录
        if not session.get('logged_in'):
            # 如果未登录，则重定向到登录页面
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha = request.form.get('captcha', '').lower()  # 将验证码转换为小写

        # 检查用户名和密码是否匹配
        if username == USERNAME and password == PASSWORD:
            # 检查验证码是否正确
            if captcha == session.get('captcha', '').lower():
                # 将用户标记为已登录，保存登录状态在会话中
                session['logged_in'] = True
                return redirect(url_for('Welcome'))
            else:
                return render_template('login.html', error='验证码错误')
        else:
            return render_template('login.html', error='用户名或密码错误')

    # GET 请求时，显示登录页面
    return render_template('login.html', error=None)


# 欢迎页面路由
@app.route('/')
@login_required
def Welcome():
    # 检查用户是否已登录
    if not session.get('logged_in'):
        # 如果未登录，则重定向到登录页面
        return redirect(url_for('login'))
    return flask.render_template('Welcome.html')


# 生成图片验证码
@app.route('/captcha')
def captcha():
    # 生成4位随机验证码
    captcha_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))

    # 将验证码保存在会话中
    session['captcha'] = captcha_text

    # 使用 captcha.image 库生成图片验证码
    image = ImageCaptcha()
    data = image.generate(captcha_text)
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'

    return response


# 注销用户
@app.route('/logout')
def logout():
    # 删除会话中的登录状态
    session.pop('logged_in', None)
    return redirect(url_for('login'))


#  404页面
@app.errorhandler(404)
def page_not_found(e):
    return 'you are worry!', 404


#  菜单页面
@app.route('/Menu')
@login_required
def Menu():
    return flask.render_template('Menu.html')


#   扫描功能页面
@app.route('/Menu/NmapFun', methods=['GET', 'POST'])
@login_required
def NmapFun():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'query_myself':
            # 获取用户的真实 IP 地址
            user_ip = request.headers.get('X-Forwarded-For')
            if user_ip:
                user_ip = user_ip.split(',')[0]  # 如果有多个 IP 地址，只获取第一个
            else:
                user_ip = request.remote_addr  # 如果 X-Forwarded-For 头不存在，则获取远程地址

            # 使用用户真实 IP 地址进行扫描
            result = query(user_ip)
            return flask.render_template('NmapFun.html', result=result)
        elif action == 'query_user_network':
            # 获取用户的真实 IP 地址
            user_ip = request.headers.get('X-Forwarded-For')
            if user_ip:
                user_ip = user_ip.split(',')[0]  # 如果有多个 IP 地址，只获取第一个
            else:
                user_ip = request.remote_addr  # 如果 X-Forwarded-For 头不存在，则获取远程地址

            # 获取用户的真实网段并进行扫描
            user_network = get_user_network(user_ip)
            result = query(user_network)
            return flask.render_template('NmapFun.html', result=result)
        elif action == 'query_other_user':
            ip = request.form.get('ip')
            result = query(ip)
            return flask.render_template('NmapFun.html', result=result)
        elif action == 'query_network':
            ip = request.form.get('network')
            result = query(ip)
            return flask.render_template('NmapFun.html', result=result)
    # 默认情况下渲染菜单页面模板
    return flask.render_template('NmapFun.html')


#   数据转换功能
@app.route('/Menu/DataConversion')
@login_required
def DataConversion():
    return flask.render_template('DataConversion.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
