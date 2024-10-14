// Cập nhật thời gian liên tục
function updateTime() {
    const currentTimeElement = document.getElementById('current-time');
    
    // Lấy thời gian hiện tại
    const now = new Date();
    const day = now.getDate().toString().padStart(2, '0');
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Tháng bắt đầu từ 0, cần cộng thêm 1
    const year = now.getFullYear();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    // Định dạng chuỗi ngày (DD/MM/YYYY) và thời gian (HH:MM:SS)
    const formattedDate = `${day}/${month}/${year}`;
    const formattedTime = `${hours}:${minutes}:${seconds}`;

    // Hiển thị ngày và thời gian trong phần tử
    currentTimeElement.textContent = `${formattedDate} ${formattedTime}`;
  }

  // Gọi hàm cập nhật ngày và thời gian mỗi giây
  setInterval(updateTime, 1000);

  // Cập nhật ngày và thời gian lần đầu khi trang được tải
  document.addEventListener('DOMContentLoaded', updateTime);
  
 