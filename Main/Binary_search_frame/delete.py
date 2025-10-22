import shutil
import os
#暂时存储图片地址

temp_path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/temp_pic'
target_path='C:/Users/LENOVO/Desktop/research/draw_bounding_box/target_pic'
#删除文件夹下面的所有文件(只删除文件,不删除文件夹)
def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)
#path_data =  temp_path
path_data =  target_path
del_file(path_data)

