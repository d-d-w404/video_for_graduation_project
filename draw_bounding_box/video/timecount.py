# 秒表计时器


# 导入模块  ===============================================================
import tkinter as tk
import time







# 按键功能实现    ==========================================================
# 时钟/计时切换
def switch_mode():
    # 声明全局变量，在局部作用域里修改
    global flag_mode

    # 显示秒表
    # 如果满足首次按秒表键，以及在停止秒表计时
    if flag_mode == 0 and not flag_switch:

        # 设置秒表初始状态，以及保存暂停后的数据
        if str_min == '' and str_sec == '' and str_mill == '':
            clock.set(value='00:00:00')
        else:
            clock.set(value=f'{str_min}:{str_sec}:{str_mill}')

        button5['text'] = '时钟'  # 按键内容更改

        # 设置按键形态
        button1['relief'] = tk.RAISED
        button2['relief'] = tk.RAISED
        button3['relief'] = tk.RAISED

        flag_mode = 1  # 时钟模式

    # 显示时钟
    # 如果满足按时钟键，以及在停止秒表计时
    elif flag_mode == 1 and not flag_switch:

        button5['text'] = '秒表'  # 按键内容更改

        # 设置按键形态
        button1.config(relief=tk.SUNKEN)
        button2.config(relief=tk.SUNKEN)
        button3.config(relief=tk.SUNKEN)

        flag_mode = 0  # 秒表模式


# 开始计时
def start():
    # 声明全局变量，在局部作用域里修改
    global flag_begin_time, flag_switch

    # 开始
    # 如果满足按的是秒表键，以及按开始键
    if flag_mode and not flag_switch:
        flag_begin_time = 1  # 开始秒表计时
        button1['text'] = '暂停'  # 更改按键内容
        flag_switch = 1  # 暂停秒表计时

    # 停止
    # 如果满足按的是秒表键，以及按暂停键
    elif flag_mode and flag_switch:
        flag_begin_time = 0  # 暂停秒表计时
        button1['text'] = '开始'  # 更改按键内容
        flag_switch = 0  # 开始秒表计时


# 实现计时功能
def start_time():
    # 声明全局变量，在局部作用域里修改
    global min, sec, mill
    global str_min, str_sec, str_mill
    global count

    # 秒表进位
    if count % 100 == 0 and count != 0:
        count = 0
        mill += 1
    if mill % 60 == 0 and mill != 0:
        mill = 0
        sec += 1
    if sec % 60 == 0 and sec != 0:
        sec = 0
        min += 1

    # 秒表数字10以下在前面补零
    if mill < 10:
        str_mill = '0' + str(mill)
    else:
        str_mill = str(mill)

    if sec < 10:
        str_sec = '0' + str(sec)
    else:
        str_sec = str(sec)

    if min < 10:
        str_min = '0' + str(min)
    else:
        str_min = str(min)

    # 显示秒表
    clock.set(value=f'{str_min}:{str_sec}:{str_mill}')

    count += 100  # 累加


# 重置
def reset():
    # 声明全局变量，在局部作用域里修改
    global flag_begin_time
    global min, sec, mill, count
    global flag_switch
    global meter_info, meter_count

    # 如果满足秒表模式
    if flag_mode:
        # 停止秒表计时
        flag_begin_time = 0

        # 秒表清零
        count = 0
        min, sec, mill = 0, 0, 0
        start_time()

        # 复位开始按键
        flag_switch = 1
        start()

        # 清空秒表计次
        meter_info = ''
        label1['text'] = ''
        meter_count = 0

        # 清空秒表计次提示语
        label2['text'] = ''


# 秒表计次
def metering():
    # 声明全局变量，在局部作用域里修改
    global meter_info, meter_count

    # 如果满足限制只能秒表内操作
    if flag_mode and flag_begin_time and meter_count < 5:

        meter_info += clock.get() + '\n'
        label1['text'] = meter_info

        meter_count += 1  # 秒表计次次数

    # 显示秒表计次上限提示语
    elif flag_mode and flag_begin_time and meter_count >= 5:
        label2['text'] = '已超过秒表计次上限！'


# 创建一个根窗口
root = tk.Tk()
# 设置窗口显示位置及大小
root.geometry(newGeometry='400x300+450+200')
# 设置窗口标题
root.title(string='秒表计时器')

# 全局变量  ===============================================================
# 创建一个可修改类型
clock = tk.StringVar()

# 定义一个模式旗帜
flag_mode = 0
# 定义开始计时旗帜
flag_begin_time = 0
# 定义一个计时 秒、分、毫秒
sec = 0
min = 0
mill = 0
# 定义一个计时 秒、分、毫秒 字符型
str_sec = ''
str_min = ''
str_mill = ''

count = 0  # 计数

# 切换旗帜
flag_switch = 0
# 存储秒表计次内容
meter_info = ''
# 秒表计次次数
meter_count = 0





# 创建一个主框架   ==========================================================
frame = tk.Frame(master=root, relief=tk.RIDGE, borderwidth=2)
# 创建一个功能框架
frame1 = tk.Frame(master=frame, )

# 创建一个标签,用于显示时间
label = tk.Label(master=frame, textvariable=clock, height=3)
# 创建一个秒表计次标签
label1 = tk.Label(master=root)
# 创建一个提示语标签
label2 = tk.Label(master=root, height=3)

# 创建功能按键
button1 = tk.Button(master=frame1, text='开始', relief=tk.SUNKEN, command=start)
button2 = tk.Button(master=frame1, text='重置', relief=tk.SUNKEN, command=reset)
button3 = tk.Button(master=frame1, text='计次', relief=tk.SUNKEN, command=metering)
button4 = tk.Button(master=frame1, text='退出', command=root.destroy)
# 计时/时钟按键
button5 = tk.Button(master=frame, text='秒表', relief=tk.FLAT, command=switch_mode)

# 功能实现  =================================================================



while True:

    # 显示主框架位置
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # 显示标签内容
    label.pack()

    # 显示时钟/秒表按键
    button5.pack()

    # 显示功能框架
    frame1.pack()

    # 显示按键
    button1.pack(side=tk.LEFT)
    button2.pack(side=tk.LEFT)
    button3.pack(side=tk.LEFT)
    button4.pack(side=tk.RIGHT)

    # 显示秒表计次
    label1.place(relx=0.5, rely=0.71, anchor=tk.N)

    # 显示秒表计次提示语
    label2.pack()

    # 实时时间
    if not flag_mode:
        clock.set(value=time.strftime('%H:%M:%S'))

    # 开始计时
    if flag_begin_time:
        start_time()

    # 刷新窗口
    root.update()
    time.sleep(0.0001)

# 保持窗口运行
root.mainloop()

