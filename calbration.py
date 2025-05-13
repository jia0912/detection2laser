import cv2
import numpy as np
import csv
import time
import serial
import os

# 初始化串口連接
<<<<<<< HEAD
ser = serial.Serial('COM3', 115200, timeout=0.1)  # 修改 COM3 為您的 Arduino 端口號
=======
ser = serial.Serial('COM7', 115200, timeout=0.1)  # 修改 COM3 為您的 Arduino 端口號
>>>>>>> b3dac3b (optimization)
time.sleep(2)  # 給 Arduino 一些啟動時間

response_received = False  # 記錄 Arduino 回應狀態

# -----------------------------
# 1. 傳送命令至 Arduino
# -----------------------------
def send_to_arduino(message):
    global response_received
    if message:
        ser.write((message + '\n').encode())
        print(f"傳送: {message}")
        response_received = False  # 重設回應狀態
        
        # 等待回應
        start_time = time.time()
        while time.time() - start_time < 2:  # 最多等待 2 秒
            if ser.in_waiting > 0:
                try:
                    response = ser.readline().decode().strip()
                except UnicodeDecodeError:
                    print("接收到非 UTF-8 格式數據，忽略...")
                    continue

                if response == "N":
                    print("Arduino 已確認接收")
                    response_received = True
                    break
                else:
                    print(f"收到未預期的回應: {response}")
            time.sleep(0.1)

        if not response_received:
            print("未收到 Arduino 回應，請檢查連接")

def generate_calibration_points(x_range, y_range, x_divisions, y_divisions):
    """
    生成校正點座標。
    :param x_range: tuple, (x_min, x_max) 振鏡 X 軸範圍
    :param y_range: tuple, (y_min, y_max) 振鏡 Y 軸範圍
    :param x_divisions: int, X 軸分割數
    :param y_divisions: int, Y 軸分割數
    :return: list, [(x1, y1), (x2, y2), ...]
    """
    x_points = np.linspace(x_range[0], x_range[1], x_divisions).astype(int)
    y_points = np.linspace(y_range[0], y_range[1], y_divisions).astype(int)
    return [(x, y) for x in x_points for y in y_points]

def send_to_galvo(x, y):
    """將振鏡命令格式化並傳送至 Arduino"""
    message="01"
    message += f"{x:04d}{y:04d}"  # 將座標格式化為 4 位數字
    send_to_arduino(message)
    time.sleep(0.5)

# -----------------------------
# 3. 拍攝校正點影像
# -----------------------------
def capture_image(camera, save_path):
    """使用相機拍攝影像並保存"""
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(save_path, frame)
        print(f"影像已保存：{save_path}")
    else:
        print("拍攝影像失敗！")

# -----------------------------
# 4. 滑鼠點擊收集影像座標
# -----------------------------
image_points = []
clicked = False

def on_mouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONDOWN and not clicked:
        print(f"滑鼠點擊影像座標: ({x}, {y})")
        image_points.append((x, y))
        clicked = True

def collect_image_point(image_path):
    global clicked, image_points
    clicked = False
    image_points = []

    image = cv2.imread(image_path)
<<<<<<< HEAD
=======
    cv2.namedWindow("calbrationImage", cv2.WINDOW_NORMAL)
>>>>>>> b3dac3b (optimization)
    cv2.imshow("calbrationImage", image)
    cv2.setMouseCallback("calbrationImage", on_mouse)

    print("請點擊影像上的雷射點...")
    while not clicked:
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    return image_points[0] if image_points else None

# -----------------------------
# 5. 保存校正檔案
# -----------------------------
def save_calibration_file(galvo_points, image_points, file_path="calibration_data.csv"):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Galvo_X", "Galvo_Y", "Image_X", "Image_Y"])
        for galvo, image in zip(galvo_points, image_points):
            writer.writerow([galvo[0], galvo[1], image[0], image[1]])
    print(f"校正檔案已保存至：{file_path}")


# -----------------------------
# 6. 計算座標轉換矩陣
# -----------------------------
def calculate_transformation_matrix(galvo_points, image_points, matrix_file="transformation_matrix.npy"):
    galvo_points_np = np.array(galvo_points, dtype="float32")
    image_points_np = np.array(image_points, dtype="float32")

    # 檢查點的數量是否一致
    if galvo_points_np.shape[0] != image_points_np.shape[0]:
        print("錯誤: 點的數量不匹配！")
        return None

    # 使用 findHomography 計算同質矩陣
    matrix, status = cv2.findHomography(image_points_np, galvo_points_np)

    # 檢查計算結果
    if matrix is not None:
        np.save(matrix_file, matrix)
        print(f"轉換矩陣已保存至：{matrix_file}")
        return matrix
    else:
        print("計算轉換矩陣失敗。")
        return None
# -----------------------------
# 7. 主程序
# -----------------------------
def main():
    # 建立儲存影像的資料夾
    image_folder = "calibration_images"
    os.makedirs(image_folder, exist_ok=True)

    camera = cv2.VideoCapture(2)
<<<<<<< HEAD
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
=======
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
>>>>>>> b3dac3b (optimization)
    # 獲取相機解析度
    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"相機解析度: {frame_width}x{frame_height}")

    if not camera.isOpened():
        print("無法打開相機！")
        return

<<<<<<< HEAD
    galvo_points = generate_calibration_points((1000,3000),(1000,3000),3,3)
=======
    galvo_points = generate_calibration_points((0,1500),(800,2200),3,3)
>>>>>>> b3dac3b (optimization)
    print("生成的振鏡校正點:", galvo_points)

    image_points = []
    for idx, (galvo_x, galvo_y) in enumerate(galvo_points):
        print(f"\n校正點 {idx + 1}/{len(galvo_points)}")
        send_to_galvo(galvo_x, galvo_y)  # 發送振鏡命令

        image_path = os.path.join(image_folder, f"calibration_image_{idx}.jpg")
        capture_image(camera, image_path)

        point = collect_image_point(image_path)
        if point is not None:
            image_points.append(point)
        else:
            print(f"校正點 {idx} 無法收集影像座標，跳過。")

    save_calibration_file(galvo_points, image_points)
    calculate_transformation_matrix(galvo_points, image_points)

    camera.release()

if __name__ == "__main__":
    main()
    send_to_arduino("00")
