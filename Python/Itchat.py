import itchat
itchat.auto_login(hotReload=True)
friends = itchat.get_friends()
print(friends)