import cv2, time

# RTSP URL
def start_rtsp(rtsp_url):
    # 创建VideoCapture对象
    # time.
    cap = cv2.VideoCapture(rtsp_url)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # print(f"视频分辨率: {width}x{height}")
    # # 获取帧率
    # fps = cap.get(cv2.CAP_PROP_FPS)

    # print(f"视频帧率: {fps} FPS")

    # 检查是否成功打开视频流
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    frame_count = 0
    # 读取视频帧
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No more frames to read.")
            break

        # 显示视频帧
        # cv2.imshow('Video Stream', frame)

        image_filename = f"frame_{frame_count}.png"

        if frame_count % 100 == 0:
            cv2.imwrite(image_filename, frame)
            print(f"Saved {image_filename}")

        frame_count += 1

        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    rtsp_url = "rtsp://admin:admin@192.168.1.10:554/channel=1/stream=0"
    start_rtsp(rtsp_url)