import subprocess
import time

def run_mqtt_handler():
    print("Running MQTT handler at: MQTT/SQLvaMQTT.py")
    return subprocess.Popen(["python", "MQTT/SQLvaMQTT.py"])

def run_mqtt_devicestatus():
    print("Running MQTT handler at: MQTT/DeviceStatus.py")
    return subprocess.Popen(["python", "MQTT/DeviceStatus.py"])

def run_app():
    print("Running app at: app.py")
    return subprocess.Popen(["python", "app.py"])

if __name__ == "__main__":
    mqtt_process = run_mqtt_handler()
    time.sleep(1)  # Chờ một chút để MQTT handler khởi động
     # Khởi động MQTT device status sau khi ứng dụng đã khởi động
    device_status_process = run_mqtt_devicestatus()
    time.sleep(1)  # Chờ một chút để Device Status khởi động
    app_process = run_app()  # Khởi động ứng dụng trước

    

    # Để chương trình không kết thúc ngay lập tức
    try:
        while True:
            time.sleep(1)  # Giữ cho chương trình chạy
    except KeyboardInterrupt:
        print("Exiting...")
        mqtt_process.terminate()  # Kết thúc quá trình mqtt_handler
        device_status_process.terminate()  # Kết thúc quá trình device status
        app_process.terminate()    # Kết thúc quá trình app
       
