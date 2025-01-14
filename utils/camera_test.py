import cv2, time
import threading

# RTSP URL
lock = threading.Lock()

def start_rtsp(rtsp_url):
    # 创建VideoCapture对象
    # time.
    cap = cv2.VideoCapture(rtsp_url)

    # 检查是否成功打开视频流
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    frame_count = 0
    # 读取视频帧
    while True:
        with lock:
            ret, frame = cap.read()
        if not ret:
            print("Error: No more frames to read.")
            break

        # 显示视频帧
        dim = (frame.shape[1]/2, 0)
        framed = cv2.resize(frame, dsize=None, fx=.5,fy=0.5)
        cv2.imshow('Video Stream', framed)
        cv2.imshow('Video Stream 2', framed)

        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()


def start_multi_rtsp():
    rtsp_url_0 = "rtsp://admin:admin@192.168.8.207:554/channel=1/stream=0"
    rtsp_url_1 = "rtsp://admin:admin@192.168.8.208:554/channel=1/stream=0"
    rtsp_url_2 = "rtsp://admin:admin@192.168.8.209:554/channel=1/stream=0"

    cap_0 = cv2.VideoCapture(rtsp_url_0)
    cap_1 = cv2.VideoCapture(rtsp_url_1)
    cap_2 = cv2.VideoCapture(rtsp_url_2)

    fx = 0.4
    fy = 0.4

    while True:
        ret_0, frame_0 = cap_0.read()
        ret_1, frame_1 = cap_1.read()
        ret_2, frame_2 = cap_2.read()

        if ret_0:
            framed_0 = cv2.resize(frame_0, dsize=None, fx=fx,fy=fy)
            cv2.imshow('207', framed_0)
        if ret_1:
            framed_1 = cv2.resize(frame_1, dsize=None, fx=fx,fy=fy)
            cv2.imshow('208', framed_1)
        if ret_2:
            framed_2 = cv2.resize(frame_2, dsize=None, fx=fx,fy=fy)
            cv2.imshow('209', framed_2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    start_multi_rtsp()

    rtsp_url = "rtsp://admin:admin@192.168.8.208:554/channel=1/stream=0"
    thread = threading.Thread(target=start_rtsp, args=(rtsp_url,))
    rtsp_url1 = "rtsp://admin:admin@192.168.8.207:554/channel=1/stream=0"
    thread1 = threading.Thread(target=start_rtsp, args=(rtsp_url1,))
    
    thread.start()
    # thread.start()
    # start_rtsp(rtsp_url)
