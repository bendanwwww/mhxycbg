import json
import pymysql
import requests
import execjs
import threading
import time
from DBUtils.PooledDB import PooledDB

class equip_spider(object):
    # 加载js
    with open('/Users/lsy/person/workspace/my_work/mhxycbg/spider/common.js', 'r', encoding='UTF-8') as file:
        result = file.read()
    common_js_code = execjs.compile(result, cwd=r'/usr/local/lib/node_modules')

    # 加载服务器列表
    with open('/Users/lsy/person/workspace/my_work/mhxycbg/spider/server.json', 'r', encoding='UTF-8') as file:
        result = file.read()
    server_json = json.loads(result)
    dict_server = {}
    for id in server_json:
        for s in server_json[id][1]:
            dict_server[s[0]] = server_json[id][0][0] + '-' + s[1]

    # 建立数据库连接
    pool = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=100,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=1,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。
        # 如：0 = None = never,
        # 1 = default = whenever it is requested,
        # 2 = when a cursor is created,
        # 4 = when a query is executed,
        # 7 = always
        host='127.0.0.1',
        port=3306,
        user='root',
        password='19951110lsy.',
        database='mhxy',
        charset='utf8'
    )

    # 加载装备类型
    dict_kind = {
                    6: "剑", 4: "枪矛", 10: "扇", 14: "刀", 5: "斧钺", 11: "魔棒", 8: "飘带", 
                    9: "爪刺", 73: "巨剑", 74: "伞", 15: "锤", 7: "双短剑", 72: "灯笼", 13: "环圈", 
                    53: "弓箭", 12: "鞭", 54: "法杖", 52: "宝珠", 20: "腰带", 17: "头盔", 21: "饰物", 
                    18: "铠甲", 59: "女衣", 58: "发钗"
                }
    attribute_names = ["魔力", "体质", "力量", "耐力", "敏捷"]

    server_ids = dict_server.keys()
    kind_ids = dict_kind.keys()

    def insert_sql(self, sql):
        conn = self.pool.connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    
    def http_get(self, header, params, url):
        return requests.get(url, headers=header, params=params, timeout = 10)

    def http_proxy_get(self, header, params, url):
        proxy_host, proxy_port = self.get_ip()
        # proxy_meta = "http://%(host)s:%(port)s" % {
        #     "host" : proxy_host,
        #     "port" : proxy_port,
        # }
        proxy_meta = "socks5://%(host)s:%(port)s" % {
            "host" : proxy_host,
            "port" : proxy_port,
        }
        proxies = {
            "http"  : proxy_meta,
            "https"  : proxy_meta
        }
        return requests.get(url, headers=header, params=params, proxies=proxies, timeout = 10)

    def get_ip(self):
        url = 'http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=2&pack=141532&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        res = requests.get(url)
        ip_info = json.loads(res.text)
        return ip_info['data'][0]['ip'], ip_info['data'][0]['port']

    def get_info(self, server_id, kind_id, price, level_start, level_end):
        sql_module = "replace into `cbg_equip` (`name`, `type`, `equip_id`, `init_shanghai`, `init_zongshang`, `init_mofa`, `init_fangyu`, `init_linli`, `init_minjie`, `init_qixue`, `addon_moli`, `addon_naili`, `addon_liliang`, `addon_tizhi`, `addon_minjie`, `tj`, `tx`, `tz`, `level`, `price`, `server_id`, `tag_json`, `e_id`, `server_name`, `type_name`, `url`) VALUES ('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, '{15}', '{16}', '{17}', {18}, {19}, {20}, '{21}', '{22}', '{23}', '{24}', '{25}');"
        url = "https://xyq.cbg.163.com/cgi-bin/recommend.py"
        for page in range(0, 100):
            print(self.dict_server[server_id] + " " + self.dict_kind[kind_id] + " " + str(page))
            params = {
                'act': 'recommd_by_role',
                'server_id': server_id,
                'page': page + 1,
                'kindid':kind_id,
                'count':100
            }
            header = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            # res = self.http_proxy_get(header, params, url)
            res = self.http_get(header, params, url)
            if res.text == '出错了:  没有找到相关的action':
                break
            res_json = json.loads(res.text)
            res_data = res_json["equips"]
            if len(res_data) == 0:
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
                self.insert_sql(sql)
    
    def start(self, kind_ids, price, level_start, level_end):
        thread_list = []
        for s in self.dict_server:
            for kind_id in kind_ids:
                c_thread = cbg_thread(self.dict_server[s], s, kind_id, price, level_start, level_end)
                c_thread.start()
                thread_list.append(c_thread)
                time.sleep(2)
                if len(thread_list) >= 2:
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
s.start([17, 20], 300.0, 0, 130)



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