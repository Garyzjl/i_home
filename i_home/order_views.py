"""__author__ - Gary"""
from datetime import datetime

from flask import Blueprint, render_template, jsonify, request, session

from i_home.models import House, Order

order_blue = Blueprint('order', __name__)


@order_blue.route('/orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


@order_blue.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@order_blue.route('/my_booking/', methods=['POST'])
def my_booking():
    house_id = request.form.get('house_id')
    house = House.query.filter_by(id=house_id).first()
    begin_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date-begin_date).days
    order.house_price = house.price
    order.amount = order.days * order.house_price
    order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@order_blue.route('/my_orders/', methods=['GET'])
def my_orders():
    orders = Order.query.filter_by(user_id=session['user_id'])
    order_list = [order.to_dict() for order in orders]
    return jsonify({'code': 200, 'msg': '请求成功', 'data': order_list})


@order_blue.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')
