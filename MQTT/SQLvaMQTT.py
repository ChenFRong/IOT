import mysql.connector
from mysql.connector import Error
import paho.mqtt.client as mqtt
import json
from datetime import datetime  # Đừng quên import datetime nếu bạn muốn sử dụng timestamp

# Thông tin cấu hình MQTT broker
MQTT_BROKER = "192.168.1.175"  # Địa chỉ MQTT broker (local hoặc remote)
MQTT_PORT = 1884  # Cổng MQTT broker
MQTT_TOPIC = "trannhung/esp8266/sensor_data"  # Chủ đề (topic) mà bạn muốn nhận dữ liệu
MQTT_USERNAME = "TranNhung"  # Tên người dùng MQTT
MQTT_PASSWORD = "B21DCCN579"  # Mật khẩu MQTT

# Hàm kết nối với MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Địa chỉ host của MySQL
            database='iot',
            user='root',
            password='nhung123456'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Hàm này sẽ được gọi khi một thông điệp mới được nhận từ MQTT
def on_message(client, userdata, message):
    data = json.loads(message.payload)
    print(f"Received data: {data}")

    # Lưu dữ liệu vào MySQL
    try:
        connection = connect_to_database()
        if connection is not None:
            cursor = connection.cursor()
            # Thêm timestamp vào dữ liệu
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO sensor_data (temperature, humidity, light, timestamp) VALUES (%s, %s, %s, %s)",
                (data['temperature'], data['humidity'], data['light'], timestamp)
            )
            connection.commit()
            cursor.close()
            connection.close()
            print("Data inserted successfully")
        else:
            print("Failed to connect to the database.")
    except mysql.connector.Error as err:
        print(f"Error: {str(err)}")

# Hàm khởi động MQTT Client
def start_mqtt_client():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.subscribe(MQTT_TOPIC)
    mqtt_client.loop_start()  # Bắt đầu loop để nhận dữ liệu

if __name__ == "__main__":
    try:
        start_mqtt_client()
        print("MQTT client started. Waiting for messages...")
        # Giữ cho chương trình chạy
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
