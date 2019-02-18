"""__author__ - Gary"""
import redis

from flask import Flask
from flask_script import Manager

from flask_session import Session


from i_home.models import db
from i_home.user_views import user_blue, login_manage
from i_home.index_views import home_blue
from i_home.order_views import order_blue

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(blueprint=user_blue, url_prefix='/ihome')
app.register_blueprint(blueprint=home_blue, url_prefix='/ihome')
app.register_blueprint(blueprint=order_blue, url_prefix='/ihome')

app.secret_key = 'vgfdfdxfgkjljkhyfg'

# 初始化redis配置
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='47.106.186.8', port=6379, password='123456')

se = Session()
se.init_app(app)

# 初始化数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manage.login_view = 'app.login'
login_manage.init_app(app)


manage = Manager(app)

if __name__ == '__main__':
    manage.run()