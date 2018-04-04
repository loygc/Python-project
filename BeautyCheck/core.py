__author__ = "susmote"

import os
import shutil
import time
from nude import Nude

start_time = time.time()
image_folder = os.path.dirname(os.path.abspath(__file__)) + "\\img\\"

os.mkdir('nudepic')
os.mkdir('commonpic')
all_pic = 0
a = 0
t = 0
f = 0

file_result = open("result.txt", "w", encoding="utf-8")
file_result.writelines("分析结果如下".center(30, '*'))
for file_name_all in os.listdir(image_folder):
    file_path_all = os.path.join(image_folder,file_name_all)
    if os.path.isdir(file_name_all):
        continue
    all_pic += 1
for file_name in os.listdir(image_folder):
    file_path = os.path.join(image_folder,file_name)
    if os.path.isdir(file_name):
        continue
    a += 1
    surplus = all_pic - a
    n = Nude(file_path)
    n.parse()

    if n.result is True:
        t += 1
        print("正在分析第%s张图片，共有%s张图片，还剩%s张图片未分析\n"%(a, all_pic, surplus))
        file_info = ('\n', file_name, "可能是一张裸体照", n.message)
        file_result.writelines(file_info)

        shutil.copy(file_path,'nudepic/')
    elif n.result is False:
        f += 1
        print("正在分析第%s张图片，共有%s+张图片，还剩%s张图片未分析\n"%(a, all_pic, surplus))
        file_info = ('\n', file_name, "是一张正常的图片", n.message)
        file_result.writelines(file_info)

        shutil.copy(file_path,'commonpic/')


file_result.writelines("\n");

file_result.writelines("总分析结果".center(30, "-"))
result_all = ("\n共有%s张图片"%a)
file_result.writelines(result_all)

file_result.writelines("\n经过我仔细的分析，得出以下结果\n")

result_nude = ("共筛选出%s张疑似裸体的照片\n" % t)
file_result.writelines(result_nude)

file_common = ("其余%s张图片都是正常的图片\n" % f)
file_result.writelines(file_common)

end_time = time.time()
spend_time = end_time-start_time

avrg_time = spend_time / a

aly_time_text = ("分析%s张图片，总共花费%s秒时间,平均每%s秒分析一张图片\n" % (a, spend_time, avrg_time))
print(aly_time_text)
file_result.writelines(aly_time_text)
file_result.writelines("此结果由计算机自动分析得出，难免会有错误")
file_result.writelines("\n作者：%s" % __author__)

file_result.close()
