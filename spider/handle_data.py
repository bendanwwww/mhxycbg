import json

with open('/Users/lsy/person/workspace/my_work/mhxycbg/spider/server.json', 'r', encoding='UTF-8') as file:
    result = file.read()
server_json = json.loads(result)
server_str = {}
for id in server_json:
    for s in server_json[id][1]:
        server_str[s[0]] = server_json[id][0][0] + '-' + s[1]
print(server_str)