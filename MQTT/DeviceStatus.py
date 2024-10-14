import paho.mqtt.client as mqtt
import json
import pymysql

# Thông tin kết nối đến cơ sở dữ liệu
db_host = 'localhost'  # Địa chỉ máy chủ cơ sở dữ liệu
db_user = 'root'  # Tên người dùng
db_password = 'nhung123456'  # Mật khẩu
db_name = 'iot'  # Tên cơ sở dữ liệu

# Kết nối đến cơ sở dữ liệu
connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

# Thông tin kết nối MQTT
mqtt_broker = "192.168.1.175"  # Địa chỉ IP của broker MQTT
mqtt_port = 1884                # Cổng của broker MQTT
mqtt_user = "TranNhung"         # Tên người dùng
mqtt_pass = "B21DCCN579"        # Mật khẩu

# Các chủ đề MQTT
topic_light_status = "trannhung/esp8266/light/status"
topic_fan_status = "trannhung/esp8266/fan/status"
topic_conditioner_status = "trannhung/esp8266/conditioner/status"

# Hàm gọi lại khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Đăng ký vào các chủ đề để nhận dữ liệu
    client.subscribe(topic_light_status)
    client.subscribe(topic_fan_status)
    client.subscribe(topic_conditioner_status)


# Hàm gọi lại khi nhận được tin nhắn
def on_message(client, userdata, msg):
    print(f"Received message from topic: {msg.topic}, payload: {msg.payload.decode()}")
    try:
        # Chuyển đổi payload thành JSON
        data = json.loads(msg.payload.decode())
        print("Data:", data)

        # Xử lý dữ liệu nhận được và cập nhật vào cơ sở dữ liệu
        with connection.cursor() as cursor:
            # Xác định thiết bị và trạng thái
            device = ''
            status = ''
            if msg.topic == topic_light_status:
                device = 'light'
                status = data['state']
                print(f"Light status: {status}")
            elif msg.topic == topic_fan_status:
                device = 'fan'
                status = data['state']
                print(f"Fan status: {status}")
            elif msg.topic == topic_conditioner_status:
                device = 'conditioner'
                status = data['state']
                print(f"Conditioner status: {status}")
                
            # Cập nhật trạng thái vào cơ sở dữ liệu
            sql = "INSERT INTO devicestatus (device, status) VALUES (%s, %s);"
            cursor.execute(sql, (device, status))

            # Lưu thay đổi vào cơ sở dữ liệu
            connection.commit()
            print("Device status updated in the database.")
    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print(f"Error updating database: {e}")

# Khởi tạo client MQTT
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_pass)  # Thiết lập tên người dùng và mật khẩu
client.on_connect = on_connect  # Thiết lập hàm gọi lại khi kết nối
client.on_message = on_message    # Thiết lập hàm gọi lại khi nhận tin nhắn

# Kết nối đến broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Bắt đầu vòng lặp
client.loop_forever()

# Đóng kết nối cơ sở dữ liệu khi không còn sử dụng
# Note: connection.close() không thể được gọi ở đây vì loop_forever() sẽ chạy mãi mãi
