import socket
import json
import time
import cv2
import numpy as np

# 設定畫面大小與 FPS
frame_width = 640
frame_height = 480
fps = 30
frame_interval = 1 / fps

# 固定物件的大小
<<<<<<< HEAD
person_width = 100
person_height = 150
=======
person_width = 20
person_height = 20
>>>>>>> b3dac3b (optimization)

# 初始位置 (將物件設置在視窗的左邊)
x1, y1 = -person_width, (frame_height // 4) - person_height // 2  # 第一個物件
x2, y2 = x1 + person_width, y1 + person_height

x3, y3 = -person_width, (frame_height // 2) - person_height // 2  # 第二個物件
x4, y4 = x3 + person_width, y3 + person_height

x5, y5 = -person_width, (frame_height * 3 // 4) - person_height // 2  # 第三個物件
x6, y6 = x5 + person_width, y5 + person_height

# 模擬 YOLO 偵測輸出
def simulate_yolo_detections():
    return [
        {"label": "person", "x1": x1, "y1": y1, "x2": x2, "y2": y2},
        {"label": "person", "x1": x3, "y1": y3, "x2": x4, "y2": y4},
        {"label": "person", "x1": x5, "y1": y5, "x2": x6, "y2": y6},
    ]

# 篩選所有 "person"
def filter_person_detections(detections):
    return [
        {"x1": det["x1"], "y1": det["y1"], "x2": det["x2"], "y2": det["y2"]}
        for det in detections if det["label"] == "person"
    ]

# 繪製檢測框到影像
def draw_detections(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = int(det["x1"]), int(det["y1"]), int(det["x2"]), int(det["y2"])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 綠色框
        cv2.putText(frame, "person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# TCP 發送座標
def send_detections_to_server(server_ip, server_port):
    global x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6  # 用 global 來修改物件位置
    conveyor_speed = 5  # 輸送帶移動的速度

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(10)  # 設定連線超時時間為10秒
        try:
            client.connect((server_ip, server_port))
            print(f"已連線到伺服器 {server_ip}:{server_port}")
            client.settimeout(None)  # 連線成功後，取消超時設定
            
            while True:
                # 模擬 YOLO 偵測
                detections = simulate_yolo_detections()
                # 篩選 "person"
                filtered_coords = filter_person_detections(detections)
                
                # 創建黑色背景的影像
                frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
                # 繪製檢測框
                draw_detections(frame, filtered_coords)
                
                # 顯示影像
                cv2.imshow("YOLO Detection Simulation", frame)

                # 移動物件，模擬輸送帶
                x1 += conveyor_speed
                x2 += conveyor_speed
                x3 += conveyor_speed
                x4 += conveyor_speed
                x5 += conveyor_speed
                x6 += conveyor_speed

                # 如果物件移動到畫面外，則重置到左邊
                if x2 > frame_width:
                    x1 = -person_width  # 重置到左邊畫面外
                    x2 = x1 + person_width

                if x4 > frame_width:
                    x3 = -person_width  # 重置到左邊畫面外
                    x4 = x3 + person_width

                if x6 > frame_width:
                    x5 = -person_width  # 重置到左邊畫面外
                    x6 = x5 + person_width

                # 發送數據
                if filtered_coords:
                    client.sendall(json.dumps(filtered_coords).encode("utf-8"))
                    print(f"發送座標:", filtered_coords)
                
                time.sleep(frame_interval)  # 模擬 30 FPS

        except socket.timeout:
            print(f"連線到伺服器 {server_ip}:{server_port} 超時，請確認伺服器是否啟動。")
        except socket.error as e:
            print(f"連線錯誤: {e}")
        finally:
            cv2.destroyAllWindows()

# 主程序
if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # 接收端 IP
    SERVER_PORT = 5000           # 接收端埠
    send_detections_to_server(SERVER_IP, SERVER_PORT)
