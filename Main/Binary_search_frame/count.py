import os

#这个函数用于统计文件夹中的文件的个数，好进行二分划分
def count_file_number(path):

    #path = './mnist_test'      # 输入文件夹地址
    files = os.listdir(path)   # 读入文件夹
    num_png = len(files)       # 统计文件夹中的文件个数
    #print(num_png)  # 打印文件个数
    return num_png

    # 输出所有文件名
    # print("所有文件名:")
    # for file in files:
    #     print(file)