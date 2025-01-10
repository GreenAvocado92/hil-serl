import cv2
import threading
import time

# 全局变量，用于存储每个摄像头的最新帧
#'camera2': None,
#'camera3': None
frames = {
    'camera1': None,
}

# 锁，用于线程安全地更新全局变量
lock = threading.Lock()

# 读取RTSP视频流并保存最新帧
def capture_frames(rtsp_url, camera_name,video_writer):
    cap = cv2.VideoCapture(rtsp_url)

    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #print(f"视频分辨率: {width}x{height}")
    if not cap.isOpened():
        print(f"Error: Could not open video stream for {camera_name}.")
        return
    #frame_count =0
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Error: No more frames to read for {camera_name}.")
            break

        # 使用锁确保线程安全地更新全局变量
        with lock:
            frames[camera_name] = frame
        
        #image_filename = f"{camera_name}_{frame_count}.png"
        #cv2.imwrite(image_filename, frame)
        
        #将图片保存成avi视频
        video_writer.write(frame)

        # 每隔一段时间保存一次帧（可选）
        time.sleep(0.05)
        #frame_count +=1

    cap.release()

# 摄像头的RTSP URL
#'camera2': "rtsp://admin:admin@192.168.8.208:554/channel=1/stream=0",
#'camera3': "rtsp://admin:admin@192.168.8.209:554/channel=1/stream=0"

rtsp_urls = {
    'camera1': "rtsp://admin:admin@192.168.8.207:554/channel=1/stream=0",
}

# 创建VideoWriter对象
#'camera2': cv2.VideoWriter('output_camera2.avi', fourcc, 20.0, (640, 480)),
#'camera3': cv2.VideoWriter('output_camera3.avi', fourcc, 20.0, (640, 480))
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用XVID编码器
video_writers = {
    'camera1': cv2.VideoWriter('output_camera1.avi', fourcc, 20.0, (2304, 1296)),
}

# 创建并启动线程
threads = []
for camera_name, rtsp_url in rtsp_urls.items():
    thread = threading.Thread(target=capture_frames, args=(rtsp_url, camera_name,video_writers[camera_name]))
    threads.append(thread)
    thread.start()

# 主线程中可以定期检查全局变量中的帧
try:
    while True:
        with lock:
            for camera_name, frame in frames.items():
                if frame is not None:
                    print(f"Latest frame from {camera_name} captured.")
                    # 可以在这里处理或保存帧
                    # 例如，保存到文件
                    # cv2.imwrite(f"latest_{camera_name}.png", frame)
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")

# 等待所有线程结束
for thread in threads:
    thread.join()

# 释放资源
for writer in video_writers.values():
    writer.release()
cv2.destroyAllWindows()