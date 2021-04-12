import sys
sys.path.append('/Users/lsy/person/workspace/my_work/mhxycbg')

import json
import execjs
import threading
import time

from data.goods_type import goods_type
from utils.server_util import server_util
from utils.http_util import http_util
from utils.db_util import db_util

class stone_spider(object):
    # 初始化外部类
    server_util_c = server_util()
    goods_type_c = goods_type()
    http_util_c = http_util()
    db_util_c = db_util()

    # 宝石类型
    dict_stone = {
        4002: "太阳石", 4003: "月亮石", 4004: "光芒石", 4005: "神秘石", 
        4010: "黑宝石", 4011: "红玛瑙", 4012: "舍利子", 4244: "星辉石", 
        4249: "翡翠石" 
    }

    def get_info(self, server_id, stone_type, level):
        url = "https://xyq.cbg.163.com/cgi-bin/recommend.py"
        params = {
                'act': 'recommd_by_role',
                'server_id': server_id,
                'page': 1,
                's_type': stone_type,
                'equip_level': level,
                'search_type': 'search_stone',
                'query_order': 'price ASC',
                'count': 1
        }
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        res = self.http_util_c.http_get(header, params, url)
        if res.text == '出错了:  没有找到相关的action':
            return
        res_json = json.loads(res.text)
        res_data = res_json["equips"]
        if len(res_data) > 0:
            return res_data[0]['price']

s = stone_spider()
min_price = s.get_info(79, 4244, 7)
print(min_price)