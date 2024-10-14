# Định nghĩa API
@app.route('/api/device_status/<string:device_name>', methods=['GET'])
def device_status(device_name):
    status = get_device_status_by_name(device_name)
    if status is not None:
        if status:
            return jsonify(status), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    else:
        return jsonify({"error": "Unable to fetch device status"}), 500