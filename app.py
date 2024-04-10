import flask
from flask import Flask

app = Flask(__name__,
            static_url_path='/static',  # 静态文件路径
            static_folder='static',
            template_folder='templates'  # 模板文件
            )


@app.route('/')
def welcome():
    return flask.render_template('welcome.html')

# @app.route('/menu')
# def menu():
#
#     return flask.render_template('')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
