import cv2
import numpy as np
import serial
import time
import os

# 初始化串口連接
<<<<<<< HEAD
ser = serial.Serial('COM3', 115200, timeout=0.1)  # 修改 COM9 為您的 Arduino 端口號
=======
ser = serial.Serial('COM7', 115200, timeout=0.1)  # 修改 COM9 為您的 Arduino 端口號
>>>>>>> b3dac3b (optimization)
time.sleep(2)  # 給 Arduino 一些啟動時間

# -----------------------------
# 傳送命令至 Arduino
# -----------------------------
def send_to_arduino(message):
    if message:
        ser.write((message + '\n').encode())
        print(f"傳送: {message}")
        time.sleep(0.01)

# -----------------------------
# 讀取轉換矩陣
# -----------------------------
def load_transformation_matrix(matrix_file="transformation_matrix.npy"):
    if not os.path.exists(matrix_file):
        print("錯誤: 找不到轉換矩陣文件。")
        return None
    return np.load(matrix_file)

# -----------------------------
# 影像座標轉換為振鏡座標
# -----------------------------
def image_to_galvo(image_point, transformation_matrix):
    if image_point is None:
        return None

    # 將影像座標轉換為齊次座標
    image_point_homogeneous = np.array([image_point[0], image_point[1], 1.0])

    # 使用轉換矩陣計算振鏡座標
    galvo_point = np.dot(transformation_matrix, image_point_homogeneous)

    # 返回振鏡座標（X, Y），並進行正規化
    return int(galvo_point[0] / galvo_point[2]), int(galvo_point[1] / galvo_point[2])

# -----------------------------
# 取得滑鼠位置的回調函數
# -----------------------------
mouse_x, mouse_y = 0, 0
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

# -----------------------------
# 主程序
# -----------------------------
def main():
    # 載入轉換矩陣
    transformation_matrix = load_transformation_matrix()

    if transformation_matrix is None:
        return

    # 捕獲影像並進行即時轉換
<<<<<<< HEAD
    camera = cv2.VideoCapture(2)
=======
    camera = cv2.VideoCapture(1)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
>>>>>>> b3dac3b (optimization)
    if not camera.isOpened():
        print("無法打開相機！")
        return

<<<<<<< HEAD
    cv2.namedWindow("realtime")
=======
    cv2.namedWindow("realtime", cv2.WINDOW_NORMAL)
>>>>>>> b3dac3b (optimization)
    cv2.setMouseCallback("realtime", mouse_callback)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("無法讀取影像")
            break

        # 顯示影像
        cv2.imshow("realtime", frame)

        # 即時捕捉滑鼠位置
        image_point = (mouse_x, mouse_y)
        print(f"滑鼠位置: {image_point}")

        # 將影像座標轉換為振鏡座標
        galvo_point = image_to_galvo(image_point, transformation_matrix)

        if galvo_point:
            print(f"轉換後的振鏡座標: {galvo_point}")
            # 發送命令到 Arduino
            send_to_arduino(f"01{galvo_point[0]:04d}{galvo_point[1]:04d}")

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    send_to_arduino("00")  # 停止雷射

if __name__ == "__main__":
    main()
