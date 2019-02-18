"""__author__ - Gary"""
import random
import re
import os
import uuid

from flask import Blueprint, render_template, jsonify, \
    session, request
from flask_login import login_user, LoginManager, login_required, logout_user

from i_home.models import User


login_manage = LoginManager()

user_blue = Blueprint('app', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整的参数'})
    # 2.验证手机号正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号不正确'})
    # 3.验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '两次密码不一致'})
    # 5.验证手机号是否已经注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已被注册，请重新注册'})
    # 创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功！'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址（不推荐）
    # 方式2：后端只生成随机参数，返回给页面，在页面中生成图片（前端做）
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIIOPASDFGHJKLZXCVBNMM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/login/', methods=['POST'])
def my_login():
    # 获取参数
    mobile = request.form.get('mobile')
    passwd = request.form.get('passwd')
    # 1.验证手机号是否正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1001, 'msg': '手机号不正确'})
    # 2.验证手机号是否已注册
    # 获取用户对象
    user = User.query.filter_by(phone=mobile).first()
    if user:
        # 3.验证密码是否正确
        if user.check_pwd(passwd):
            login_user(user)   # 实际实现的是登录标识符设置 session['user_id'] = user.id 操作
            return jsonify({'code': 200, 'msg': '请求成功'})
        else:
            return jsonify({'code': 1003, 'msg': '密码不正确'})
    else:
        return jsonify({'code': 1002, 'msg': '手机号未注册，请先注册'})


@login_manage.user_loader
def load_user(id):
    return User.query.get(id)


@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    # 获取用户基本信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/logout/', methods=['GET'])
def logout():
    # 退出当前用户
    logout_user()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


@user_blue.route('/update_info/', methods=['PATCH'])
def update_info():
    # 接收图片，并保存
    icon = request.files.get('avatar')
    name = request.form.get('name')
    if icon:
        # 获取用户对象
        user = User.query.get(session['user_id'])
        # 获取项目文件根路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 获取媒体文件的路径
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
        # 随机生成图片的名称
        filename = str(uuid.uuid4())
        a = icon.mimetype.split('/')[-1:][0]
        ico_name = filename + '.' + a
        # 拼接图片的地址
        path = os.path.join(MEDIA_DIR, ico_name)
        if user.avatar:
            DEL_DIR = MEDIA_DIR + '/' + user.avatar
            os.remove(DEL_DIR)
            # 保存
            icon.save(path)
            # 修改用户头像avatar字段
            user.avatar = ico_name
            user.add_update()
        else:
            # 保存
            icon.save(path)
            # 修改用户头像avatar字段
            user.avatar = ico_name
            user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})
    if name:
        # 判断用户名是否存在
        if User.query.filter(User.name == name).count():
            return jsonify({'code': 1004, 'msg': '用户名已存在'})
        # 获取用户对象
        user = User.query.get(session['user_id'])
        user.name = name
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blue.route('/real_auth/', methods=['PATCH'])
def real_auth():
    # 获取参数
    name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    # 1.姓名验证不能超过6个字符
    if not re.fullmatch(r'^[\u4e00-\u9fa5]{2,6}$', name):
        return jsonify({'code': 1005, 'msg': '姓名不符合规范'})
    # 2.验证身份证号码是否正确
    if not re.match('^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$', id_card):
        return jsonify({'code': 1006, 'msg': '身份证号码不正确'})
    # 3.验证身份证号是否存在
    user = User.query.filter_by(id_card=id_card).first()
    if user:
        return jsonify({'code': 1007, 'msg': '身份证号码已存在'})
    # 创建实名认证信息
    user = User.query.get(session['user_id'])
    user.id_name = name
    user.id_card = id_card
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/auth_info/', methods=['GET'])
@login_required
def auth_info():
    user = User.query.get(session['user_id'])
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_auth_dict()})



