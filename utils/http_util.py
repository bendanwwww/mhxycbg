import requests

class http_util(object):
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