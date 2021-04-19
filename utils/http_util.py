import requests
import os
import json

class http_util(object):
    def http_get(self, header, params, url):
        return requests.get(url, headers=header, params=params, timeout = 10)

    def http_proxy_get(self, header, params, url):
        self.set_proxy()
        return requests.get(url, headers=header, params=params, timeout = 10)

    def set_proxy(self):
        # url = 'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=141532&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        # proxy = requests.get(url).text
        os.environ["http_proxy"] = "http://42.56.35.211:4240"
        os.environ["https_proxy"] = "https://42.56.35.211:4240"

    def get_cbg_info_proxy(self, params, retry):
        url = "https://xyq.cbg.163.com/cgi-bin/recommend.py"
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        res = self.http_get(header, params, url)
        if res.text == '出错了:  没有找到相关的action':
            return []
        res_json = json.loads(res.text)
        num = 0
        while "equips" not in res_json:
            if num > retry:
                return []
            self.set_proxy()
            res = self.http_get(header, params, url)
            res_json = json.loads(res.text)
            num += 1
        return res_json["equips"]