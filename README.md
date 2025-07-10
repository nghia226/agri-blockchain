# agri-blockchain
# 🧾 IBM Food Trust - Truy xuất nguồn gốc nông sản

Ứng dụng web mô phỏng hệ thống truy xuất chuỗi cung ứng nông sản theo mô hình IBM Food Trust.  
Được xây dựng bằng **Flask + Bootstrap 5** và lưu trữ dữ liệu sản phẩm bằng công nghệ blockchain đơn giản.

---

## 🚀 Tính năng nổi bật

- ✅ Đăng ký sản phẩm nông sản lên blockchain
- 📜 Timeline chuỗi cung ứng: Đóng gói, vận chuyển, tiêu thụ
- 📎 Upload tài liệu PDF (chứng nhận, hóa đơn...)
- ⚠️ Cảnh báo nếu sản phẩm thu hoạch quá 7 ngày chưa tiêu thụ
- 🔍 Tìm kiếm sản phẩm theo tên hoặc mã ID
- 📱 Tạo mã QR để quét truy xuất thông tin sản phẩm
- 💾 Lưu blockchain ra file `blockchain_data.json`
- 🌐 Deploy online bằng Render.com

---
#Cấu trúc thư mục
├── app.py                  # Flask app chính
├── blockchain.py           # Blockchain class đơn giản
├── blockchain_data.json    # Lưu dữ liệu blockchain (tự tạo khi chạy)
├── templates/              # HTML templates (Jinja2 + Bootstrap 5)
├── uploads/                # Lưu file PDF người dùng tải lên
├── requirements.txt        # Danh sách thư viện
├── render.yaml             # Cấu hình deploy Render

#💡 Ý tưởng thực hiện
Dự án mô phỏng cơ chế hoạt động của nền tảng IBM Food Trust – ứng dụng blockchain để minh bạch hóa chuỗi cung ứng nông sản, phục vụ người tiêu dùng và nhà sản xuất.

Người thực hiện
Khanh Huyen
📫 https://github.com/nghia226
