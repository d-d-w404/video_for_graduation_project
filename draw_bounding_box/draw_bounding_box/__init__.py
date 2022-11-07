import cv2
import pdb
from time import time
import os
from voc_xml import VOCAnnotation, object_xml


flag = 1
flag1 = 1


# def get_fname():
#     return str(time()).replace('.', '_')


store_url=r'C:\Users\LENOVO\Desktop\research\draw_bounding_box\store'

#这个函数主要从“跟踪所得到的物件位置”文件中获得相关信息，并生成list
url=r'C:\Users\LENOVO\Desktop\research\draw_bounding_box\1.txt'
def fl():
    #open('/home/zf/frame/1.txt', mode='r', encoding=None)
    open(url, mode='r', encoding=None)
    # file 包含文件名的字符串，可以是绝对路径，可以是相对路径。
    # mode 一个可选字符串，用于指定打开文件的模式。默认值 r 表示文本读。
    # encoding 文本模式下指定文件的字符编码
    with open(url, mode="r", encoding=None) as fb:
        bt1 = fb.readlines()
        #bt1是整个文件的list，每一行是一个元素
        for i in range(len(bt1)):
            bt1[i] = bt1[i].split(',')
        #此时的bt1就是一个[[],[]...]
        return bt1

bt = fl()


get_cur_dir = lambda path: os.path.abspath(path).split('/')[-1]


# def write_voc_pascal(img, box_params, path=store_url, img_fmt='.jpg'):
#     fname = get_fname()
#     img_name = fname + img_fmt
#     path1 = os.path.join(path, img_name)
#     print(path)
#     print(path1)
#     cv2.imwrite(os.path.join(path, img_name), img)
#     voc = VOCAnnotation(get_cur_dir(path), img_name, os.path.abspath(path),
#                         img.shape[1], img.shape[0], img.shape[2])
#     for param in box_params:
#         voc.add_object(object_xml(param[0], int(param[1][0]), int(param[1][1]), int(param[1][2]), int(param[1][3])))
#     voc.write_to_file(os.path.join(path, fname + '.xml'))


class DrawBoundingBox():
    def __init__(self, get_box_params, get_image, post_calc=None, window_title='Bounding Box', quit_key='q',
                 font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, font_color=(255, 0, 0), line_type=2,
                 box_thickness=2, box_color=(0, 0, 255), pred_box_color=(0, 255, 0),
                 img_dir=store_url):
        '''
        post_calc - function - first argument will be an image (numpy array)
        second arguement will be a list of tuples representing the actual list 
        of labels and boxes for the image third argument will also be a list 
        of tuples representing the predicted list of labels and boxes for the image
        post_calc(img, y_box_params, box_params)

        get_box_params - function - takes in an image (numpy array) should 
        return a list of tuples where the first element of the tuple is the 
        label of the box and the second 
        element is a list of 4 numbers representing the coordinates of the
        bounding box [x_top_left, y_top_left, x_bottom_right, y_bottom_right]

        get_image - function - should return a tuple - first element should
        be the next image (numpy array). second element should be a list of 
        tuples where each entry is of form (label, bbox)
        '''
        self.get_box_params, self.get_image = get_box_params, get_image
        self.WINDOW_TITLE, self.quit_key, self.img_dir = window_title, quit_key, img_dir
        self.box_color, self.pred_box_color = box_color, pred_box_color
        self.post_calc = post_calc
        self.font_args = {'font': font, 'font_scale': font_scale,
                          'font_color': font_color, 'line_type': line_type,
                          'box_thickness': box_thickness, 'box_color': box_color}

    def run(self):
        self.cv_loop(self._draw_box, quit_key=self.quit_key)

    # cv_loop_on_key(self._draw_box, quit_key='q', next_key='n')

    #这个函数就是给一张图片，然后画框，给注释，然后保存
    def draw_label_and_box(self,img, iname, label, color, box, font_args):
        # 这个函数中的几个参数就是1.txt中的参数
        print(box)
        # path = '/home/zf/draw_bounding_box/frame/'
        path = store_url
        img_name = str(iname) + '.jpg'
        path1 = os.path.join(path, img_name)
        print(path)
        print(path1)
        #    print(box[2])
        if color == "green":
            font_args['box_color'] = (0, 255, 0)
        if color == "red":
            font_args['box_color'] = (0, 0, 255)

        img1 = cv2.rectangle(img, tuple((int(box[0]), int(box[1]))), tuple((int(box[2]), int(box[3]))),
                             font_args['box_color'], font_args['box_thickness'])

        cv2.putText(img, label, tuple((int(box[0]), int(box[1]))),
                    font_args['font'], font_args['font_scale'],
                    font_args['font_color'], font_args['line_type'])
        cv2.imwrite(os.path.join(path, img_name), img1)

    #这个_draw_box画的是每张图片,相较于上面的函数，这个函数不会关注具体调用什么去画框，做标注，而是
    #如何通过文件信息找到相关的图片，并且把相关文件中的参数和图片联系起来
    def _draw_box(self):
        global flag
        global flag1
        #j = 0
        #j暂时没用
        list1 = []
        #list1中存储的就是一个帧中的ball和human,有的时候只有一个
        img = self.get_image()
        for i in range(len(bt)):
            if flag == int(bt[i][0]):
                list1.append(bt[i][0:8])
                #j = j + 1
#-----------------------------画框的部分------------------------------------------------------

        if len(list1):
            # print("1111")
            print(list1)
            #
            #list1 = list(list1)#这一步似乎感觉不需要
            # print("hello")
            # print(list1)
            if img is not None:
                # arg = bt[flag1][2:6]
                # print(arg)
                box_params = self.get_box_params(img)
                # print(box_params)
                #            write_voc_pascal(img, box_params, path=self.img_dir)
                self.font_args['box_color'] = self.box_color
                # list(map(lambda arg: draw_label_and_box(img, arg[0],
                #                                       arg[1], self.font_args), box_params))
                print(list1[0][0:5])
                print(list1[0][3])
                print("--------")
                list(map(lambda arg: print(arg), list1))
                print("--------")
                list(map(lambda arg: self.draw_label_and_box(img, arg[0], arg[2], arg[3],
                                                        arg[4:8], self.font_args), list1))
                '''
                这里需要注意一下map(lambda )这个东西，list1有的时候是[[],[]]这样的就会将两个[]里的东西都使用
                此时的arg[0]会有两个值，分别对应human和ball
                有的时候是[[]]的，就会使用一个
                
                解释就是map是对我输入的列表中的每个元素都进行操作，也就是说此时的arg就是list1这个列表的每个元素
                而每个元素又是一个列表，所以可以用arg[0]，而不是arg[0][1]之类的
                '''
                # draw_label_and_box(img, bt[flag1][0], 'a',
                #                 arg, self.font_args)

                #            list(map(lambda arg: draw_label_and_box(img, arg[0],
                #                                                    arg[1], self.font_args), y_box_params))
                #            self.post_calc(img, y_box_params, box_params)

                flag1 = flag1 + 1
#---------------------------------------------------------------------------------------
        cv2.imshow(self.WINDOW_TITLE, img)
        flag = flag + 1
        list1.clear()

    # 这个是对每一帧做循环
    def cv_loop(self,run_func, quit_key='q'):
        while True:
            if (cv2.waitKey(2) & 0xFF) == ord(quit_key):
                cv2.destroyAllWindows()
                break
            else:
                run_func()

    def cv_loop_on_key(self,run_func, quit_key='q', next_key='n'):
        run_func()
        while True:
            key_pressed = (cv2.waitKey(2) & 0xFF)
            if key_pressed == ord(quit_key):
                cv2.destroyAllWindows()
                break
            elif key_pressed == ord(next_key):
                run_func()


#        y_box_params = self.get_image()


def image_from_cv(read):
    # return None if ret == False else return frame
    ret, frame = read()
    return frame if ret else None


class DrawBoundingBoxOnNext(DrawBoundingBox):
    def __init__(self, get_box_params, get_image, post_calc=None, window_title='Bounding Box', quit_key='q',
                 font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, font_color=(0, 0, 0), line_type=2,
                 box_thickness=2, box_color=(0, 0, 255), pred_box_color=(0, 255, 0), img_dir='.', next_key='n'):
        '''
        get_box_params - function - takes in an image (numpy array) should 
        return a list of tuples where the first element of the tuple is the 
        label of the box and the second 
        element is a list of 4 numbers representing the coordinates of the
        bounding box [x_top_left, y_top_left, x_bottom_right, y_bottom_right]

        get_image - function - should return a tuple - first element should
        be the next image (numpy array). second element should be a list of 
        tuples where each entry is of form (label, bbox)

        next_key - character - next image is obtained and its bounding box is displayed
                when the user clicks this key
        '''
        super().__init__(get_box_params, get_image, window_title=window_title,
                         quit_key=quit_key, font=font, font_scale=font_scale, font_color=font_color,
                         line_type=line_type, box_thickness=box_thickness, box_color=box_color,
                         pred_box_color=pred_box_color, img_dir=img_dir, post_calc=post_calc)
        self.next_key = next_key

    def run(self):
        self.cv_loop_on_key(self._draw_box, quit_key=self.quit_key, next_key=self.next_key)


class OpenCVBoundingBox(DrawBoundingBox):
    def __init__(self, get_box_params, cam_num=0, window_title='Bounding Box', post_calc=None, quit_key='q',
                 font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, font_color=(0, 0, 0), line_type=2,
                 box_thickness=2, box_color=(0, 0, 255), pred_box_color=(0, 255, 0), img_dir='.'):
        self.vcap = cv2.VideoCapture(cam_num)

        def get_image():
            return image_from_cv(self.vcap.read)

        super().__init__(get_box_params, get_image, window_title=window_title, post_calc=post_calc,
                         quit_key=quit_key, font=font, font_scale=font_scale, font_color=font_color,
                         line_type=line_type, box_thickness=box_thickness, box_color=box_color,
                         pred_box_color=pred_box_color, img_dir=img_dir)


class DrawBoundingBoxOnFolder(DrawBoundingBoxOnNext):
    def __init__(self, folder_path, get_box_params, window_title='Bounding Box', post_calc=None, quit_key='q',
                 font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, font_color=(0, 0, 0), line_type=2,
                 box_thickness=2, box_color=(0, 0, 255), pred_box_color=(0, 255, 0), img_dir='.', next_key='n'):
        self.folder_path = folder_path
        get_image = None  # TODO - replace with proper implementation
        super().__init__(get_box_params, get_image, window_title=window_title, post_calc=post_calc,
                         quit_key=quit_key, font=font, font_scale=font_scale, font_color=font_color,
                         line_type=line_type, box_thickness=box_thickness, box_color=box_color,
                         pred_box_color=pred_box_color, img_dir=img_dir)
