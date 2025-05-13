import socket
import json
import serial
import numpy as np
import time
import os
import cv2

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
    x = int(galvo_point[0] / galvo_point[2])
    y = int(galvo_point[1] / galvo_point[2])

    # 只返回範圍在 0 到 4095 之間的座標
<<<<<<< HEAD
    if 0 <= x <= 4095 and 0 <= y <= 4095:
=======
    if 0 <= x <= 2000 and 700 <= y <= 2300:
>>>>>>> b3dac3b (optimization)
        return x, y
    else:
        return None

# 繪製座標並顯示影像
<<<<<<< HEAD
def draw_coordinates_on_image(coords_list, frame_width=640, frame_height=480):
=======
def draw_coordinates_on_image(coords_list, frame_width=2560, frame_height=1440):
>>>>>>> b3dac3b (optimization)
    # 創建黑色背景的影像
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    
    # 繪製接收到的座標
    for coords in coords_list:
        x1, y1 = coords['x1'], coords['y1']
        x2, y2 = coords['x2'], coords['y2']
        
        # 顯示座標點
        cv2.circle(frame, (x1, y1), 5, (0, 255, 0), -1)  # 綠色圓點
        cv2.circle(frame, (x2, y2), 5, (0, 255, 0), -1)
        
        # 顯示框
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 綠色框
    
    # 顯示影像
<<<<<<< HEAD
=======
    cv2.namedWindow("Received Coordinates", cv2.WINDOW_NORMAL)
>>>>>>> b3dac3b (optimization)
    cv2.imshow("Received Coordinates", frame)
    cv2.waitKey(1)  # 這裡等待1毫秒即可，因為會在每個循環中更新

# 接收並處理座標
def receive_and_process_coordinates(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(1)
        print(f"伺服器已啟動，等待連線 ({host}:{port}) ...")
        
        conn, addr = server.accept()
        print(f"已連線到客戶端 {addr}")
        
        # 載入轉換矩陣
        transformation_matrix = load_transformation_matrix()

        with conn:
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    
                    # 解碼並解析接收到的 JSON 資料
                    coords_list = json.loads(data.decode("utf-8"))
                    print("接收到原始座標:", coords_list)
                    
                    # 繪製接收到的座標並顯示影像
                    draw_coordinates_on_image(coords_list)

                    # 對每一組座標進行轉換並持續傳送
                    for coords in coords_list:
                        x1, y1 = coords['x1'], coords['y1']
                        x2, y2 = coords['x2'], coords['y2']
                        
                        # 轉換每個座標點
                        transformed_point1 = image_to_galvo((x1, y1), transformation_matrix)
                        transformed_point2 = image_to_galvo((x2, y2), transformation_matrix)

                        # 僅發送符合範圍條件的座標
                        if transformed_point1 and transformed_point2:
                            print(f"轉換後的振鏡座標: {transformed_point1}{transformed_point2}")
                            send_to_arduino(f"07{transformed_point1[0]:04d}{transformed_point1[1]:04d}{transformed_point2[0]:04d}{transformed_point2[1]:04d}")

                    # 等待下一組座標
                    print("等待下一組座標...")

                except json.JSONDecodeError:
                    print("接收到無效的 JSON 資料")
                except Exception as e:
                    print(f"發生錯誤: {e}")

# 主程序
if __name__ == "__main__":

    HOST = "0.0.0.0"  # 接收所有網路介面連線
    PORT = 5000       # 伺服器埠
    receive_and_process_coordinates(HOST, PORT)
