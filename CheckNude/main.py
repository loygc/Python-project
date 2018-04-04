__author__ = "susmote"

from nude import Nude
import os


IMAGE_ROOT = ROOT = os.path.dirname(os.path.abspath(__file__)) + "\\imags\\"
for file_name in os.listdir(IMAGE_ROOT):
    file_path = os.path.join(IMAGE_ROOT,file_name)
    if os.path.isdir(file_name):
        continue
    n = Nude(file_path)
    n.parse()
    print(n.skin_map)
    if n.result is True:
        print(file_name,"可能是一张裸体照",n.message)
    elif n.result is False:
        print(file_name,"是一张正常的图片",n.message)



