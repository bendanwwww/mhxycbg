import itchat

class wx_util(object):
    # enableCmdQR=True，允许在cmd命令行显示二维码
    # hotReload=True，允许短期内可以不需要重复登陆
    itchat.auto_login(hotReload=True)

    def send_msg(self):
        to_name = itchat.search_friends(name="鲍聪浩")
        print(to_name)
        # 发送文本消息
        for i in range(10):
            itchat.send('测试中。。。',toUserName=to_name[0]['UserName'])
        #
        # # 发送表情包
        # file_img = 'biaoqingbao.jpg'
        # itchat.send_image(file_img,toUserName=to_name[0]['UserName'])

        # search_chatrooms 获取通讯录中群聊列表 update=True 会获取实时有信息的群
        # myroom = itchat.get_chatrooms(update=True)
        # print(myroom)
        # to_room = itchat.search_chatrooms(name='群聊名称')
        # # print(to_room)
        # for i in range(10):
        #     itchat.send('需要发送的文字信息',toUserName=to_room[0]['UserName'])



s = wx_util()
s.send_msg()