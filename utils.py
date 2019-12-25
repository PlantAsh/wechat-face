# -*-coding:utf-8 -*-
import requests
import json
import threading
import time
import os

import properties as pro
from wechat_error import WechatError

token = ''


def img_download(url, name):
    r = requests.get(url)
    with open('images/{}-{}.jpg'.format(name, time.strftime("%Y_%m_%d%H_%M_%S", time.localtime())), 'wb') as fd:
        fd.write(r.content)
    if os.path.getsize(fd.name) >= 1048576:
        return 'large'
    # print('namename', os.path.basename(fd.name))
    return os.path.basename(fd.name)


def get_access_token():
    """获取access_token,100分钟刷新一次"""

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(pro.wechat_app_id, pro.wechat_secret)
    print("微信获取access_token请求：" + str(url))
    r = requests.get(url)
    parse_json = json.loads(r.text)
    print("微信获取access_token返回：" + str(parse_json))
    global token
    if 'access_token' not in parse_json:
        timer = threading.Timer(6000, get_access_token)
        timer.start()
        return
    token = parse_json['access_token']
    timer = threading.Timer(6000, get_access_token)
    timer.start()


def img_upload(media_type, name):
    global token
    print("token：" + str(token))
    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (token, media_type)
    try:
        files = {'media': open('{}'.format(name), 'rb')}
        r = requests.post(url, files=files)
        parse_json = json.loads(r.text)
        print("微信新增临时素材返回：" + str(parse_json))
    except Exception:
        raise WechatError('微信接口失效，请稍后重试')
    if 'media_id' not in parse_json:
        return 'false'
    return parse_json['media_id']


get_access_token()
