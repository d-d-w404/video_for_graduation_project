#这个脚本主要是为了修改我的文件命名

import os #导入模块
filename = 'C:/Users/Wander/Desktop/output/' #文件地址
list_path = os.listdir(filename)  #读取文件夹里面的名字

# filename_='C:/Users/Wander/Desktop/0'
# list_path_=os.listdir(filename_)
#
# # for index_ in list_path_:
# #     list_path__=os.listdir(index_)
# #     for index__ in list_path__:
# #         name = os.path.basename(index__)
# #
# #         path = os.path.dirname(index__)
# #         print('------------------')
# #         print(path)
# #         print(name)
# #         print('------------------')

import os

import shutil

# os.walk

# todo 获取文件夹中的所有文件

# root 是文件夹地址

# dirs 是文件夹相对地址

# files 是文件名列表



def trans_specific_file(path,new_path,suffix):
    for root ,dirs,files in os.walk(path):
        for name in files:
            if os.path.splitext(name)[1].lower() == suffix.lower():
                #aim_file_path= os.path.join(root,name)

                name=name.split('.')[0]
                aim_file_path = os.path.join(filename, name+".txt")
                print(aim_file_path)

                for index in list_path:
                    thisname = index.split('.')[0]   #split字符串分割的方法 , 分割之后是返回的列表 索引取第一个元素[0]
                    if thisname==name:
                        print("right")
                        new_name=root+'/'+name+".txt"
                        new_name=new_name.replace('/','$')
                        new_name = new_name.replace(':', '#')
                        print(new_name)
                        new_file_path = os.path.join(new_path,new_name)
                        #print(root)
                        print(new_file_path)
                        shutil.copyfile(aim_file_path,new_file_path)

                # new_file_path = os.path.join(new_path,name)
                # shutil.copyfile(aim_file_path,new_file_path)
                #print(root)
                print('正在复制文件 '+name+'...')
    return print('文件备份完成')



if __name__ == "__main__":
    suffix ='.mp4'
    #path='C:/Users/Wander/Desktop/0/'
    path = 'C:/Users/Wander/Desktop/Graduation_Project/train/2021-12-16/2021-12-10/0/'
    new_path = 'C:/Users/Wander/Desktop/newoutput/'
    trans_specific_file(path,new_path,suffix)


# for index in list_path:  #list_path返回的是一个列表   通过for循环遍历提取元素
#     name = index.split('.')[0]   #split字符串分割的方法 , 分割之后是返回的列表 索引取第一个元素[0]
#     kid = index.split('.')[-1]   #[-1] 取最后一个
#     path = filename + '\\' + index
#     new_path = filename + '\\'  + name +  '.' + kid
#     # os.rename(path, new_path) #重新命名
#
#     print(new_path)
#
# print('修改完成')
