import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os

#global varibles
previous_points_1 = np.array([[]])
previous_points_2 = np.array([[]])
point_1 = ()
point_2 = ()
old_frame_grey = 0
first_point = False
second_point = False
cap = cv2.VideoCapture(0)
#global varibles


def main():
    global previous_points_1, previous_points_2,old_frame_grey, cap
    img_name = "frame"
    cv2.namedWindow(img_name)
    cv2.setMouseCallback(img_name, select_point)
    LKP= dict(winSize = (13,13), maxLevel = 15, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TermCriteria_COUNT, 40, 0.03)) #Luca kandace parameter
    while True:
        ret, img = cap.read() #read the frame from the camera
        key = cv2.waitKey(1)
        frame_grey = get_gray(img)
        if first_point and second_point:
            draw_circle(img, point_1)
            current_point_1, status, error = cv2.calcOpticalFlowPyrLK(old_frame_grey, frame_grey, previous_points_1, None, **LKP)
            previous_points_1 = current_point_1
            x_1,y_1 = current_point_1.ravel()
            draw_circle(img,(x_1,y_1),color = (0, 255, 0),thickness= -1)
            #print(previous_points_1)

            draw_circle(img, point_2)
            current_point_2, status, error= cv2.calcOpticalFlowPyrLK(old_frame_grey, frame_grey, previous_points_2,None, **LKP)
            previous_points_2 = current_point_2
            x_2,y_2 = current_point_2.ravel()
            draw_circle(img,(x_2,y_2),color = (0, 255, 255),thickness= -1)
            old_frame_grey = frame_grey.copy()
        cv2.imshow(img_name, img) #show the current frame

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




def select_point(event,x,y, flags,params):
    #The function detect if the first point or the second point is selected.
    global first_point, second_point, point_1,point_2, previous_points_1, previous_points_2,old_frame_grey, cap
    if event == cv2.EVENT_LBUTTONDOWN:
        if first_point is False:
            first_point = True
            point_1 = (x, y)
            previous_points_1 = np.array([[x,y]], dtype = np.float32)
        else:
            second_point =True
            point_2 = (x, y)
            previous_points_2 = np.array([[x,y]], dtype = np.float32)
            ret, frame = cap.read()  # read the frame from the camera
            old_frame_grey = get_gray(frame)

def get_gray(frame):
    # Input is the image
    # Return the gray version of the image
    return cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


def draw_line(img, start_point, end_point, color = (255,0 ,0 ), thickness = 5):
    # start and end point are tuple (x,y)
    # color : Color of the shape. for BGR, pass it as a tuple, eg: (255,0,0) for blue. For grayscale, just pass the scalar value.
    # thickness : if -1 is passed for closed figures like circles, it will fill the shape, default thickness = 1.
    cv2.line(img, start_point, end_point, color, thickness)


def draw_rectangle(img, start_point, end_point, color = (255,0 ,0 ), thickness = 3):
    # start and end point are tuple (x,y), it's the position of the left upper point and right lower point
    # color : Color of the shape. for BGR, pass it as a tuple, eg: (255,0,0) for blue. For grayscale, just pass the scalar value.
    # thickness : if -1 is passed for closed figures like circles, it will fill the shape, default thickness = 1.
    cv2.rectangle(img, start_point, end_point, color, thickness)


def draw_circle(img, center_point, radius = 6, color = (255, 0, 0), thickness = 3):
    # center point is the center of the circle (x,y). radius is the radius of the circle.
    # If -1 is passed for closed figures like circles, it will fill the shape. default thickness
    # color : Color of the shape. for BGR, pass it as a tuple, eg: (255,0,0) for blue. For grayscale, just pass the scalar value.
    # thickness : if -1 is passed for closed figures like circles, it will fill the shape, default thickness = 1.
    cv2.circle(img, center_point,radius, color, thickness)


def draw_text(img, left_corner, font_size, color = (255, 255, 255), thickness = 2):
    #left corner is the tuple (x,y)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'OpenCV', left_corner, font, font_size, color, thickness, cv2.LINE_AA)


def real_time():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # Our operations on the frame come here
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def facial():
    cap = cv2.VideoCapture(0)
    # 获取外接摄像头

    ''' cv.VideoWriter参数（视频存放路径，视频存放格式，fps帧率，视频宽高）
        注意点1：OpenCV只支持avi的格式，而且生成的视频文件不能大于2GB，而且不能添加音频
        注意点2：若填写的文件名已存在，则该视频不会录制成功，但可正常使用
    '''
    print(cap.isOpened())
    # 检测是否摄像头正常打开:成功打开时，isOpened返回ture
    classifier_face = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    # 定义分类器（人脸识别）
    classifier_eye = cv2.CascadeClassifier("haarcascade_eye.xml")
    # 定义分类器（人眼识别）
    classifier_mouth = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
    # 定义分类器（嘴巴识别）
    key = cv2.waitKey(1)

    while True:
        # 取得cap.isOpened()返回状态为True,即检测到人脸
        # img = cv2.imread("/Users/funny/Downloads/img/pp.png")
        ret, img = cap.read()
        '''第一个参数ret的值为True或False，代表有没有读到图片
           第二个参数是frame，是当前截取一帧的图片
        '''
        faceRects_face = classifier_face.detectMultiScale(img, 1.2, 2, cv2.CASCADE_SCALE_IMAGE, (20, 20))
        # 检测器：detectMultiScale参数（图像，每次缩小图像的比例，匹配成功所需要的周围矩形框的数目，检测的类型，匹配物体的大小范围）
        # 键盘等待
        if len(faceRects_face) > 0:
            # 检测到人脸
            for faceRect_face in faceRects_face:
                x, y, w, h = faceRect_face
                # 获取图像x起点,y起点,宽，高
                h1 = int(float(h / 1.5))
                # 截取人脸区域高度的一半位置，以精确识别眼睛的位置
                intx = int(x)
                inty = int(y)
                intw = int(w)
                inth = int(h)
                # 转换类型为int，方便之后图像截取
                my = int(float(y + 0.7 * h))
                # 截取人脸区域下半部分左上角的y起点，以精确识别嘴巴的位置
                mh = int(0.4 * h)
                # 截取人脸区域下半部分高度，以精确识别嘴巴的位置
                img_facehalf = img[inty:(inty + h1), intx:intx + intw]
                img_facehalf_bottom = img[my:(my + mh), intx:intx + intw]
                '''img获取坐标为，【y,y+h之间（竖）：x,x+w之间(横)范围内的数组】
                   img_facehalf是截取人脸识别到区域上半部分
                   img_facehalf_bottom是截取人脸识别到区域下半部分
                '''
                cv2.rectangle(img, (int(x), my), (int(x) + int(w), my + mh), (0, 255, 0), 2, 0)
                '''矩形画出区域 rectangle参数（图像，左顶点坐标(x,y)，右下顶点坐标（x+w,y+h），线条颜色，线条粗细）
                    画出人脸识别下部分区域，方便定位
                '''
                faceRects_mouth = classifier_mouth.detectMultiScale(img_facehalf_bottom, 1.1, 1,
                                                                    cv2.CASCADE_SCALE_IMAGE, (5, 20))
                # 嘴巴检测器
                cv2.rectangle(img, (int(x), int(y)), (int(x) + int(w), int(y) + int(h1)), (0, 255, 0), 2, 0)
                # 画出人脸识别上部分区域，方便定位
                faceRects_eye = classifier_eye.detectMultiScale(img_facehalf, 1.2, 2, cv2.CASCADE_SCALE_IMAGE, (20, 20))
                # 检测器识别眼睛
                if len(faceRects_eye) > 0:
                    # 检测到眼睛后循环
                    eye_tag = []
                    # 定义一个列表存放两只眼睛坐标
                    for faceRect_eye in faceRects_eye:
                        x1, y1, w1, h2 = faceRect_eye
                        cv2.rectangle(img_facehalf, (int(x1), int(y1)), (int(x1) + int(w1), int(y1) + int(h2)),
                                      (0, 255, 0), 2, 0)
                        # 画出眼睛区域
                        a = ((inty + y1), (inty + y1 + h2), (intx + x1), (intx + x1 + w1))
                        # 定义a变量获取眼睛坐标，现在img顶点位置已经改变，需要加上intx和inty的值才可以
                        eye_tag.append(a)
                        # 通过append存入数组a中
        cv2.imshow('video', img)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()









main()