__author__ = "susmote"

import os
import shutil


image_folder = os.path.dirname(os.path.abspath(__file__)) + "\\img\\"

for file_name in os.listdir(image_folder):
    file_path = os.path.join(image_folder,file_name)
    if os.path.isdir(file_name):
        continue
    shutil.move(file_path,'movres/')