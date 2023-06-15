import subprocess
import time
from ppadb.client import Client as AdbClient
import threading

# Hàm thực thi lệnh ADB
def run_adb_command(command):
    adb_command = ['adb'] + command.split()
    process = subprocess.Popen(adb_command, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode('utf-8')

# Kết nối thiết bị Android với máy tính
def connect_device():
    run_adb_command('devices')

# Bật sự kiện chạm trên thiết bị
def enable_touch_events():
    run_adb_command('shell settings put system pointer_location 1')

# Mô phỏng lần nhấp chuột tại tọa độ (x, y)
def simulate_click(x, y):
    run_adb_command(f'shell input tap {x} {y}')
    
def text(text):
    # Chạy lệnh ADB để gửi văn bản vào thiết bị
    command = f'shell input text "{text}"'
    run_adb_command(command)

# Hàm chạy công việc click
def run_click(device):
    time.sleep(10)
    print(f"Running click on device: {device.serial}")
    # Mô phỏng lần nhấp chuột tại tọa độ (300, 500)
    simulate_click(150, 900)
    time.sleep(2)
    simulate_click(550, 930)
    time.sleep(2)
    simulate_click(650, 450)
    time.sleep(2)
    simulate_click(490, 2340)
    time.sleep(2)
    text("test adb")
    time.sleep(2)
    simulate_click(1005, 1644)

# Hàm chạy scrcpy
def run_scrcpy(device):
    subprocess.call("scrcpy", shell=True)

# Kết nối thiết bị Android với máy tính
connect_device()

# Bật sự kiện chạm trên thiết bị
enable_touch_events()

# Tạo danh sách các thiết bị đã kết nối
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

# Số lượng luồng
thread_num = min(1, len(devices))

# Tạo và khởi chạy các luồng
threads = []
for i in range(thread_num):
    device = devices[i]
    t1 = threading.Thread(target=run_scrcpy, args=(device,))
    t0 = threading.Thread(target=run_click, args=(device,))
    t0.start()
    t1.start()
    t0.join()
    t1.join()
