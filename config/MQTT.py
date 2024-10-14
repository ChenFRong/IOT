# config_mqtt.py

# Thông tin kết nối đến MQTT Broker
MQTT_BROKER = "192.168.1.175"  # Địa chỉ IP của MQTT broker
MQTT_PORT = 1884  # Cổng MQTT
MQTT_USERNAME = "TranNhung"  # Tên đăng nhập
MQTT_PASSWORD = "B21DCCN579"  # Mật khẩu

# Chủ đề MQTT
TOPIC_LIGHT = "trannhung/esp8266/light"
TOPIC_FAN = "trannhung/esp8266/fan"
TOPIC_CONDITIONER = "trannhung/esp8266/conditioner"
TOPIC_ALL = "trannhung/esp8266/all"
TOPIC_LIGHT_STATUS = "trannhung/esp8266/light/status"
TOPIC_FAN_STATUS = "trannhung/esp8266/fan/status"
TOPIC_CONDITIONER_STATUS = "trannhung/esp8266/conditioner/status"
TOPIC_ALL_STATUS = "trannhung/esp8266/all/status"
TOPIC_SENSOR_DATA = "trannhung/esp8266/sensor_data"
