"""__author__ - Gary"""
# 创建图片唯一名称

import os
import uuid


def only_name(icon):
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
    return path, ico_name