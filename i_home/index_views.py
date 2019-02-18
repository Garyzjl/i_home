"""__author__ - Gary"""
from utils.function import only_name

from flask import Blueprint, render_template, jsonify, request, session

from i_home.models import Area, Facility, House, HouseImage

home_blue = Blueprint('home', __name__)


@home_blue.route('/index/')
def index():
    return render_template('index.html')


@home_blue.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


@home_blue.route('/my_house/', methods=['GET'])
def my_house():
    house = House.query.filter_by(user_id=session['user_id']).all()
    house_info = []
    for i in range(len(house)):
        house_info.append(house[i].to_dict())
    return jsonify({'code': 200, 'msg': '请求成功', 'data': house_info})


@home_blue.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@home_blue.route('/facility/', methods=['GET'])
def facility():
    facility = Facility.query.all()
    facilites = []
    for i in range(len(facility)):
        facilites.append(facility[i].to_dict())
    return jsonify({'code': 200, 'msg': '请求成功', 'data': facilites})


@home_blue.route('/area/', methods=['GET'])
def area():
    area = Area.query.all()
    areas = []
    for i in range(len(area)):
        areas.append(area[i].to_dict())
    return jsonify({'code': 200, 'msg': '请求成功', 'data': areas})


@home_blue.route('/get_house/', methods=['POST'])
def get_house():
    # 获取参数
    home = request.form.to_dict()
    facilities = request.form.getlist('facility')
    # 获取区域对象
    area = request.form.get('area_id')
    a = Area.query.filter_by(id=area).first()
    # 创建新房源
    house = House()
    house.title = home['title']
    house.price = home['price']
    house.area_id = a.id
    house.address = home['address']
    house.room_count = home['room_count']
    house.acreage = home['acreage']
    house.unit = home['unit']
    house.capacity = home['capacity']
    house.beds = home['beds']
    house.deposit = home['deposit']
    house.min_days = home['min_days']
    house.max_days = home['max_days']
    house.user_id = session['user_id']
    for i in facilities:
        facility = Facility.query.filter_by(id=i).first()
        house.facilities.append(facility)
    house.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': house.to_full_dict()})


@home_blue.route('/house_image/', methods=['PATCH'])
def house_image():
    # 接收图片，并保存
    image = request.files.get('house_image')
    house_id = request.form.get('house_id')
    url = only_name(image)
    # 保存
    image.save(url[0])
    # 获取参数对象
    h_image = HouseImage()
    # 修改字段
    h_image.house_id = house_id
    h_image.url = '/static/media/' + url[1]
    h_image.add_update()
    all_image = HouseImage.query.filter_by(house_id=house_id).all()
    images = []
    for i in range(len(all_image)):
        images.append(all_image[i].url)
    if len(all_image) >= 1:
        house = House.query.filter_by(id=house_id).first()
        house.index_image_url = all_image[0].url
        h_image.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': images})


@home_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@home_blue.route('/house_detail/', methods=['GET'])
def house_detail():
    house_id = request.args.get('house_id')
    house = House.query.filter_by(id=house_id).first()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': house.to_full_dict()})