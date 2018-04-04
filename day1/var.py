# -*- coding:utf-8 -*-
# Author susmote
import getpass
print("hello world!!!")
U_name = input("请输入你的姓名：")
password = getpass.getpass("请输入你的密码：")
info = '''
-----------information----------
usename:%s
password:%s
-------------end----------------
'''%(U_name,password)
print(info)