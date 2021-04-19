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

class equip_spider(object):
    # 初始化外部类
    server_util_c = server_util()
    goods_type_c = goods_type()
    http_util_c = http_util()
    db_util_c = db_util()

    # 加载js
    with open('/Users/lsy/person/workspace/my_work/mhxycbg/data/common.js', 'r', encoding='UTF-8') as file:
        result = file.read()
    common_js_code = execjs.compile(result, cwd=r'/usr/local/lib/node_modules')

    attribute_names = ["魔力", "体质", "力量", "耐力", "敏捷"]
    dict_server = server_util_c.get_server_list()
    dict_kind = goods_type_c.dict_kind

    server_ids = dict_server.keys()
    kind_ids = dict_kind.keys()

    def get_info(self, server_id, kind_id, price, level_start, level_end):
        sql_module = "replace into `cbg_equip` (`name`, `type`, `equip_id`, `init_shanghai`, `init_zongshang`, `init_mofa`, `init_fangyu`, `init_linli`, `init_minjie`, `init_qixue`, `addon_moli`, `addon_naili`, `addon_liliang`, `addon_tizhi`, `addon_minjie`, `tj`, `tx`, `tz`, `level`, `price`, `server_id`, `tag_json`, `e_id`, `server_name`, `type_name`, `url`) VALUES ('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, '{15}', '{16}', '{17}', {18}, {19}, {20}, '{21}', '{22}', '{23}', '{24}', '{25}');"
        for page in range(0, 100):
            print(self.dict_server[server_id] + " " + self.dict_kind[kind_id] + " " + str(page))
            params = {
                'act': 'recommd_by_role',
                'server_id': server_id,
                'page': page + 1,
                'kindid':kind_id,
                'count':100
            }
            res_data = self.http_util_c.get_cbg_info_proxy(params, 5)
            if len(res_data) == 0:
                print("数据为空")
                break
            for data in res_data:
                if float(data["price"]) > price:
                    continue
                if int(data["level"]) < level_start or int(data["level"]) > level_end:
                    continue

                attr_info = [0, 0, 0, 0, 0]
                tj = ''
                tx = ''
                tz = ''
                if data["other_info"] is not None or data["other_info"] != '':
                    other_info = self.common_js_code.call("decode_desc", data["other_info"])
                    other_info_json = json.loads(other_info)
                    add_melt_attrs = other_info_json["add_melt_attrs"]

                    for attr in add_melt_attrs:
                        attr_split = attr.split(' ')
                        if attr_split[0] in self.attribute_names:
                            attr_info[self.attribute_names.index(attr_split[0])] = attr_split[1]
                    desc = other_info_json["desc"]
                    desc_tj = desc.split('#c4DBAF4')
                    if len(desc_tj) > 1:
                        desc_tj_tx_str = ''.join(''.join(''.join(desc_tj[1:]).split('制造者')[:1]).split('开运孔数')[:1]).replace('#', '').replace('Y', '').replace('r', '').replace('W', '').replace('G', '')
                        tj_tx_str_split = desc_tj_tx_str.split('特效：')
                        if len(tj_tx_str_split) == 1:
                            tj_tz_split = tj_tx_str_split[0].split('套装效果：')
                            if len(tj_tz_split) == 2:
                                tz = tj_tz_split[1]
                            tj = tj_tz_split[0].replace('特技：', '')
                        else:
                            if tj_tx_str_split[0] != '':
                                tj = tj_tx_str_split[0].replace('特技：', '')
                            tx_tz_split = tj_tx_str_split[1].split('套装效果：')
                            if len(tx_tz_split) == 2:
                                tz = tx_tz_split[1]
                            tx = tx_tz_split[0].replace('特效：', '')
                url = "http://xyq.cbg.163.com/equip?s="+ str(server_id) +"&eid="+ data["eid"] +"&view_loc=equip_list|" + data["tag_key"]
                sql = sql_module.format(data["equip_name"], kind_id, data["equipid"], data["init_damage_raw"], data["init_damage"], data["mofa"], data["init_defense"], data["lingli"], data["minjie"], data["init_hp"], attr_info[0], attr_info[3], attr_info[2], attr_info[1], attr_info[4], tj, tx, tz, data["level"], data["price"], server_id, data["tag_key"], data["eid"], self.dict_server[server_id], self.dict_kind[kind_id], url)
                self.db_util_c.execute_sql(sql)
    
    def start(self, kind_ids, price, level_start, level_end):
        thread_list = []
        for s in self.dict_server:
            for kind_id in kind_ids:
                c_thread = cbg_thread(self.dict_server[s], s, kind_id, price, level_start, level_end)
                c_thread.start()
                thread_list.append(c_thread)
                # time.sleep(1)
                if len(thread_list) >= 1:
                    while thread_list:
                        thread_list.pop().join()


class cbg_thread(threading.Thread):
    def __init__(self, thread_name, server_id, kind_id, price, level_start, level_end):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.server_id = server_id
        self.kind_id = kind_id
        self.price = price
        self.level_start = level_start
        self.level_end = level_end
    def run(self):
        print ("开始线程: " + self.thread_name)
        s = equip_spider()
        s.get_info(self.server_id, self.kind_id, self.price, self.level_start, self.level_end)
        print ("结束线程: " + self.thread_name)

s = equip_spider()
# s.start([6], 10000000000000000000.0, 0, 160)
s.start([18], 300.0, 130, 130)

# proxy_host, proxy_port = s.get_ip()
# proxy_meta = "http://%(host)s:%(port)s" % {
#     "host" : proxy_host,
#     "port" : proxy_port,
# }
# proxies = {
#     "http"  : proxy_meta,
#     "https"  : proxy_meta
# }
# cookies = {
#                 'kuaishou.merchant.guard_st': 'ChprdWFpc2hvdS5tZXJjaGFudC5ndWFyZC5zdBKwAZE4YnjlQrG8Aaf5fr6lqRL0Cp7X7sQ4j6eapyaB6UVTdR9hBRPYoubcbfj5dlkFd4PyuYcdU8eZ3tE_8wE0GOzmrZH56kCb2KITWkhGX8RLaZFogh1AGTSiKWOL0Ipw1cg-RRIEny8kwaPnc5G4tLO6klN5NyrhYjxdI7z6pVKIncmgOQlYRYePlICbaSVyz5y2lsBrda82qHQ3yjk2su8-uQrF82OJuxyMrskDpCh_GhKdiHHQOZJX8h-sVT_H10927YkiIO9tYuDJWPi1WejtCPHV4k9rVfiYw2xlz0wkdfS_XkwDKAowAQ',
#                 'did': 'web_153c6482d2aa4abebace13592eb6641bc734',
#                 'userId': '1761432505'
#             }
# res = requests.get('https://kwaishop-guard.test.gifshow.com/rest/pc/guard/users/getUserInfo', proxies=proxies, cookies=cookies)
# print(res.text)