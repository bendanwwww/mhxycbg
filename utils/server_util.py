import json

class server_util(object):
    # 服务器列表
    dict_server = {}

    def init(self):
        # 加载服务器列表
        with open('/Users/lsy/person/workspace/my_work/mhxycbg/data/server.json', 'r', encoding='UTF-8') as file:
            result = file.read()
        server_json = json.loads(result)
        for id in server_json:
            for s in server_json[id][1]:
                self.dict_server[s[0]] = server_json[id][0][0] + '-' + s[1]

    def get_server_list(self):
        if len(self.dict_server) == 0:
            self.init()
        return self.dict_server