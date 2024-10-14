

const ctx = document.getElementById('sensor-chart').getContext('2d');
const sensorChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Thời gian cập nhật
        datasets: [
            {
                label: 'Temperature (°C)',
                borderColor: '#ff3333',
                backgroundColor: 'rgba(255, 51, 51, 0.2)',
                data: [], // Dữ liệu nhiệt độ
                fill: true,
                borderWidth: 2
            },
            {
                label: 'Humidity (%)',
                borderColor: '#1446F7',
                backgroundColor: 'rgba(20, 70, 247, 0.2)',
                data: [], // Dữ liệu độ ẩm
                fill: true,
                borderWidth: 2
            },
            {
                label: 'Light (lx)',
                borderColor: '#F27405',
                backgroundColor: 'rgba(242, 116, 5, 0.2)',
                data: [], // Dữ liệu ánh sáng
                fill: true,
                borderWidth: 2
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Value'
                },
                min: 0,
                max: 3500 // Giới hạn tối đa cho độ sáng
            }
        }
    }
});

function updateCanvasSize() {
    const chartContainer = document.querySelector('.device-container'); // Ô trắng chứa biểu đồ
    const containerWidth = chartContainer.clientWidth;
    const containerHeight = chartContainer.clientHeight;

    // Cập nhật kích thước canvas
    sensorChart.canvas.parentNode.style.width = 500 + 'px'; // Cập nhật chiều rộng
    sensorChart.canvas.parentNode.style.height = 450 + 'px'; // Cập nhật chiều cao
    sensorChart.resize(); // Gọi hàm resize của Chart.js
}

// Hàm để lấy dữ liệu cảm biến từ API và cập nhật biểu đồ
function fetchSensorData() {
    $.ajax({
        url: '/ten_sensor_data', // URL API để lấy 10 dữ liệu gần nhất
        method: 'GET',
        success: function(data) {
            console.log(data);
            // const timestamps = data.map(item => formatTimestamp(item.timestamp));

            // const temperatures = data.map(item => item.temperature);
            // const humidities = data.map(item => item.humidity);
            // const lights = data.map(item => item.light);
            const timestamps = data.map(item => formatTimestamp(item.timestamp)).reverse(); // Đảo ngược mảng thời gian
            const temperatures = data.map(item => item.temperature).reverse(); // Đảo ngược mảng nhiệt độ
            const humidities = data.map(item => item.humidity).reverse(); // Đảo ngược mảng độ ẩm
            const lights = data.map(item => item.light).reverse(); // Đảo ngược mảng ánh sáng


            // Cập nhật dữ liệu biểu đồ
            sensorChart.data.labels = timestamps;
            sensorChart.data.datasets[0].data = temperatures; // Nhiệt độ
            sensorChart.data.datasets[1].data = humidities;   // Độ ẩm
            sensorChart.data.datasets[2].data = lights;       // Ánh sáng

            sensorChart.update(); // Cập nhật biểu đồ sau khi thay đổi dữ liệu
        },
        error: function(err) {
            console.error('Error fetching sensor data:', err);
        }
    });
    function formatTimestamp(timestamp) {
        // console.log(timestamp);
        const date = new Date(timestamp);
        const hours = date.getUTCHours().toString().padStart(2, '0'); // Sử dụng getUTCHours để lấy giờ UTC
        const minutes = date.getUTCMinutes().toString().padStart(2, '0');
        const seconds = date.getUTCSeconds().toString().padStart(2, '0');
        const day = date.getUTCDate().toString().padStart(2, '0');
        const month = (date.getUTCMonth() + 1).toString().padStart(2, '0'); // Tháng từ 0-11 nên cần cộng thêm 1
        const year = date.getUTCFullYear();

        // Định dạng theo 'hh:mm:ss dd/MM/yyyy'
        return `${hours}:${minutes}:${seconds} ${day}/${month}/${year}`;
    }
    

}

// Gọi fetchSensorData lần đầu để hiển thị dữ liệu ngay khi tải trang
fetchSensorData();

// Cập nhật biểu đồ mỗi 2 giây
setInterval(fetchSensorData, 2000);

// Gọi hàm để cập nhật kích thước canvas
updateCanvasSize();

