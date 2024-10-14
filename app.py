from flask import Flask, render_template, jsonify, request
import mysql.connector
from config.SQL import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import paho.mqtt.publish as publish
from datetime import datetime
import logging
from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Đường dẫn tới tài liệu swagger.json (đặt file swagger.json ở thư mục gốc hoặc trong thư mục tĩnh)
SWAGGER_URL = '/swagger'  # Đường dẫn để truy cập giao diện Swagger UI
API_URL = '/static/json/swagger.json'  # Đường dẫn tới file swagger.json của bạn

# Thiết lập Swagger UI Blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Cấu hình tuỳ chỉnh cho Swagger UI
        'app_name': "IOT API"
    }
)

# Đăng ký Swagger UI Blueprint vào Flask
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Định nghĩa route để lấy file swagger.json
@app.route('/static/json/<path:filename>')
def send_swagger_json(filename):
    return send_from_directory('static/json', filename)


# Kết nối MySQL
def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# Lấy dữ liệu cảm biến mới nhất cho trang index
def get_latest_sensor_data():
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT temperature, humidity, light, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
        sensor_data = cursor.fetchone()

        if not sensor_data:
            return {'temperature': 'N/A', 'humidity': 'N/A', 'light': 'N/A', 'timestamp': 'N/A'}

        return sensor_data
    
# Hàm để lấy 10 dữ liệu cảm biến mới nhất cho biểu đồ
def get_ten_latest_sensor_data():
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
        sensor_data = cursor.fetchall()  # Lấy tất cả 10 bản ghi

        if not sensor_data:
            return {'error': 'No data found'}
        
        return sensor_data




# # Lấy dữ liệu cảm biến với phân trang cho trang datasensor
# def get_sensor_data_with_pagination(offset=0, limit=20):
#     with connect_db() as connection:
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT id, temperature, humidity, light, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT %s OFFSET %s", (limit, offset))
#         sensor_data = cursor.fetchall() or []

#         # Định dạng lại timestamp cho từng hàng dữ liệu
#         for row in sensor_data:
#             row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

#         return sensor_data
    
# Lấy dữ liệu cảm biến từ sensor_data
def get_sensor_data_all():
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, temperature, humidity, light, timestamp FROM sensor_data ORDER BY timestamp DESC")
        sensor_data = cursor.fetchall() or []

        # Định dạng lại timestamp cho từng hàng dữ liệu
        for row in sensor_data:
            row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        return sensor_data



# Ghi lịch sử hành động vào bảng actionhistory
def log_action_to_db(device, action):
    with connect_db() as connection:
        cursor = connection.cursor()
        query = "INSERT INTO actionhistory (devices, action, time) VALUES (%s, %s, %s)"
        cursor.execute(query, (device, action, datetime.now()))
        connection.commit()



# Trang chủ
@app.route('/', methods=['GET'])
def home():
    sensor_data = get_latest_sensor_data()
    return render_template('index.html', sensor_data=sensor_data)

# API trả về dữ liệu cảm biến mới nhất
@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    sensor_data = get_latest_sensor_data()
    return jsonify(sensor_data)

# API trả về 10 dữ liệu cảm biến mới nhất cho biểu đồ 
@app.route('/ten_sensor_data', methods=['GET'])
def get_ten_sensor_data():
    sensor_data = get_ten_latest_sensor_data()
    return jsonify(sensor_data)

# # API trả về dữ liệu cảm biến với phân trang
# @app.route('/sensor_data_page', methods=['GET'])
# def sensor_data_page():
#     offset = int(request.args.get('offset', 0))  # Lấy tham số offset từ query string, mặc định là 0
#     limit = int(request.args.get('limit', 20))   # Lấy tham số limit từ query string, mặc định là 20
#     sensor_data = get_sensor_data_with_pagination(offset, limit)
#     return jsonify(sensor_data)

# API trả về tất cả dữ liệu 
@app.route('/sensor_data_all', methods=['GET'])
def sensor_data_page_all():
       # Lấy tham số limit từ query string, mặc định là 20
    sensor_data = get_sensor_data_all()
    return jsonify(sensor_data)


# Trang hiển thị dữ liệu cảm biến
@app.route('/sensor_data_view', methods=['GET'])
def sensor_data_view():
    # offset = int(request.args.get('offset', 0))
    # limit = 20  # Giới hạn số lượng bản ghi trả về là 20
    sensor_data = get_sensor_data_all()
    return render_template('/pages/datasensor/datasensor.html', sensor_data=sensor_data)


# Hàm tìm kiếm dữ liệu sensor
def search_datasensor(search_value='', search_field='all'):
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)

        # Nếu search_field là 'all', tìm kiếm trên tất cả các cột
        if search_field == 'all':
            query = """
            SELECT * FROM sensor_data
            WHERE id LIKE %s OR temperature LIKE %s OR humidity LIKE %s OR light LIKE %s OR timestamp LIKE %s
            """
            params = (f'%{search_value}%', f'%{search_value}%', f'%{search_value}%', f'%{search_value}%', f'%{search_value}%')
        elif search_field == 'ID':
            query = """
            SELECT * FROM sensor_data
            WHERE id LIKE %s
            """
            params = (f'%{search_value}%',)
        elif search_field == 'Temperature':
            query = """
            SELECT * FROM sensor_data
            WHERE temperature LIKE %s
            """
            params = (f'%{search_value}%',)
        elif search_field == 'Humidity':
            query = """
            SELECT * FROM sensor_data
            WHERE humidity LIKE %s
            """
            params = (f'%{search_value}%',)
        elif search_field == 'Light':
            query = """
            SELECT * FROM sensor_data
            WHERE light LIKE %s
            """
            params = (f'%{search_value}%',)
        elif search_field == 'timestamp':
            query = """
            SELECT * FROM sensor_data
            WHERE timestamp LIKE %s
            """
            params = (f'%{search_value}%',)
        else:
            return []

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Định dạng lại thời gian nếu là timestamp
        for row in results:
            row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row['timestamp'], datetime) else row['timestamp']

        return results
    
    
# tìm kiếm sensor data
@app.route('/search_sensordata', methods=['GET'])
def search_datasensor_view():
    search_value = request.args.get('queries', '')  # Giá trị tìm kiếm từ người dùng
    search_field = request.args.get('field', 'all')  # Trường tìm kiếm, mặc định là 'all'

    # Gọi hàm tìm kiếm dữ liệu sensor
    sensor_data = search_datasensor(search_value, search_field)
    return jsonify(sensor_data)  # Trả về dữ liệu dưới dạng JSON



# Điều khiển thiết bị qua MQTT
@app.route('/toggle_device/<device>/<action>', methods=['POST'])
def toggle_device_action(device, action):
    device = device.lower()  # Chuyển device về chữ thường
    action = action.lower()  # Chuyển action về chữ thường

    mqtt_topic_map = {
        'light': 'trannhung/esp8266/light',
        'fan': 'trannhung/esp8266/fan',
        'air_conditioner': 'trannhung/esp8266/conditioner'
    }

    if device in mqtt_topic_map:
        try:
            publish.single(
                mqtt_topic_map[device],
                action,
                hostname="192.168.1.175",
                port=1884,
                auth={'username': "TranNhung", 'password': "B21DCCN579"}
            )
            log_action_to_db(device, action)
            return jsonify({'status': 'success', 'device': device, 'action': action}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Device not supported'}), 400
    
# Hàm để lấy trạng thái thiết bị theo tên

# Lấy trạng thái thiết bị
def get_device_status(device):
    with connect_db() as connection:
        cursor = connection.cursor()
        sql = "SELECT device, status, last_update FROM devicestatus WHERE device = %s ORDER BY last_update DESC LIMIT 1;"
        cursor.execute(sql, (device,))
        return cursor.fetchone()

  
#lấy trạng thái mới nhất của thiết bị 
@app.route('/api/device_status/<string:device_name>', methods=['GET'])
def device_status(device_name):
    status = get_device_status(device_name)
    if status is not None:
        device, device_status, last_update = status
        return jsonify({
            "device": device,
            "status": device_status,
            "last_update": last_update.strftime('%Y-%m-%d %H:%M:%S') if last_update else None  # Định dạng thời gian
        }), 200
    else:
        return jsonify({"error": "Device not found"}), 404  # Thông báo không tìm thấy thiết bị

# Lấy dữ liệu lịch sử hành động từ MySQL, bao gồm cả id
def get_action_history():
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, devices, action, time FROM actionhistory ORDER BY time DESC")
        action_history = cursor.fetchall() or []

        # Định dạng lại timestamp cho từng hàng dữ liệu
        for row in action_history:
            row['time'] = row['time'].strftime('%Y-%m-%d %H:%M:%S')

        return action_history

# Trang hiển thị lịch sử hành động với id
@app.route('/actionhistory', methods=['GET'])
def action_history_view():
    action_history = get_action_history()  # Lấy dữ liệu từ MySQL
    return render_template('/pages/Actionhistory/actionhistory.html', action_history=action_history)

# Hàm tìm kiếm actionhistory
def search_action_history(search_value='', search_field='all'):
    with connect_db() as connection:
        cursor = connection.cursor(dictionary=True)

        if search_field == 'all':
            query = """
            SELECT * FROM actionhistory
            WHERE id LIKE %s OR devices LIKE %s OR action LIKE %s OR time LIKE %s
            """
            params = (f'%{search_value}%', f'%{search_value}%', f'%{search_value}%', f'%{search_value}%')
        elif search_field == 'time':
            query = """
            SELECT * FROM actionhistory
            WHERE time LIKE %s
            """
            params = (f'%{search_value}%',)
        else:
            return []

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Định dạng lại thời gian nếu là timestamp
        for row in results:
            row['time'] = row['time'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row['time'], datetime) else row['time']

        return results

@app.route('/search_actionhistory', methods=['GET'])
def search_action_history_view():
    search_value = request.args.get('queries', '')  # Giá trị tìm kiếm
    search_field = request.args.get('field', 'all')  # Trường tìm kiếm, mặc định là 'all'

    action_history = search_action_history(search_value, search_field)
    return jsonify(action_history)

@app.route('/Profile', methods=['GET'])
def profile_view():
    # Thông tin tĩnh cần hiển thị
    user_info = {
        'Full Name': 'Trần Thị Phương Nhung',
        'Student ID': 'B21DCCN579',
        'Class': 'B21CNPM2',
        # Thêm các thông tin khác nếu cần
    }
    
    # Trả về template với thông tin người dùng
    return render_template('/pages/Profile/profile.html', user_info=user_info)

if __name__ == '__main__':
    app.run(debug=True)
