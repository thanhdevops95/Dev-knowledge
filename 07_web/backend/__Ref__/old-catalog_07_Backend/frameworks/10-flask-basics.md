# 🐍 Flask (Python) Basics — Vua Của Sự Tối Giản (Micro-framework)

> `[BEGINNER]` — Prerequisite: (Nắm vững Python căn bản `05-Languages/python/01-python-basics.md` và Cấu trúc REST API).
> Trái ngược hoàn toàn với sự Đồ sộ, áp đặt nguyên tắc và Bào mòn Trí não của Java Spring Boot, hay C# ASP.NET. Có những dự án bạn CHỈ CẦN DỰNG ĐÚNG 1 CÁI ĐƯỜNG DẪN API để Trả về 1 Câu Lệnh Chào, hay Cầm cái Lõi Model AI Machine Learning Ráp ném lên Web cho Khách tải Ảnh xem Khuôn mặt. Flask là Câu trả lời Hoàn Hảo nhất của Thế giới Python!

---

## Tại sao (WHY) Flask Lại Được Tôn Thờ Bởi Dân AI Và Data Science?

Trong Python, bạn có gã Khổng Lồ **Django**. Django đẻ ra sẵn Database, Phân quyền Admin, HTML Form... giống hệt Laravel (PHP). 
Nhưng nếu bạn là Kỹ sư AI, bạn vừa train xong model Nhận Diện Mèo bằng PyTorch/TensorFlow, bạn Đâu Cần Ba Cái Phân Quyền Vớ Vẩn Đấy? Bạn chỉ Cần 1 Cái Giao Thép Thô Dựng Dịch Vụ Mạng (Web Server) Cực Nhanh Nhất Có Thể Để bọc Code AI:

**Flask Là "Micro-framework"**: 
Lúc Cài Xong, Nó Không Có Hỗ Trợ SQL Database, Cắm Sẵn Form Gì Cả! Bộ Lõi Của Nó Chưa Tới 1 MB! Nó Chỉ Cho Bạn Cái **Hệ Dẫn Đường (Routing)** Và Chấm Hết. Gọn Gãy Rệt Tính Toán, Trong Sạch. Muốn Chèn Toán Cụ Vào, Mua Đồ Gì Ra Dãy Thêm (Ví Dụ Cài SQL SQLAlchemy Ráp Thêm Đuôi Gây API API Đo).

---

## 1. Bản Đồ Mạch Thép Phá Lệnh Tạo Toàn Trọng 1 Web Bằng Đúng 5 Lệnh Python

Đỉnh Cao Rút Gọt Code Của Python Kép Xuyên: `pip install Flask`. Cắm Đoạn Mã Vào File `ung_dung_chinh.py`:

```python
from flask import Flask, jsonify

# 1. Khai Báo Rạp Khung Gọng Thẳng Kéo Khởi App!
app_tao_oanh = Flask(__name__)

# 2. Phép Bùa Ngải (Decorators Của Mệnh Oanh Python) Giống `@GetMapping` Dưới Java Òa API
@app_tao_oanh.route('/api/chao', methods=['GET'])
def chao_nghia_khach():
    # Đi Thô Vỏ Object Python Trả JSON Phẳng Của Hàm jsonify
    return jsonify({
        "Thong_Diep": "Hello AI Bằng Flask",
        "TrangThang": "Cực Mở Kênh Oanh Mất 5 Dòng Text Code!"
    })

# 3. Chạy Server Nghe Đi Gắn Lệnh Của Chóp Cõi (Port 5000)
if __name__ == '__main__':
    app_tao_oanh.run(debug=True)
```

**Thành Quả Rạch Mạch Dịch Đo Báo Đường:** `python ung_dung_chinh.py`. REST API Đã Lên Sóng Trong 5 Dòng! 

---

## 2. Parameter Dấu Định Router Nằm Giao Oanh Kì Oác (Path Variables & Tóm Data Từ POST)

Kéo Data Chứa Khung Khách Nhận:

```python
from flask import request

# API Báo Lệnh Nhận Thẳng File Đi Dòng POST Oanh Oác Text
@app_tao_oanh.route('/api/ai/nhan-dien-anh', methods=['POST'])
def nhan_dien():
    # 1. Đo Dữ Liệu Máy JSON Bắt Lệnh Request Nhấn Text Json Front Trực Oanh Ném Về
    data_nhan_duoc = request.get_json()
    link_anh = data_nhan_duoc.get("URL_ANH_CUA_BAN")

    if link_anh is None:
        return jsonify({"Lỗi Cú": "Hô Nhập Web App Link Đi"}), 400
        
    # [Tưởng Tượng: Chóp Gọi Hàm Ráp Cục AI Mô Phỏng Trình Model PyTorch Phẳng Giả Ở Đây...]
    ket_qua = "Đây Là Con Chó Pug"

    return jsonify({"AI_Dap_An": ket_qua}), 200

# API Lạc Đảo Xuyên URL Trách (Param) `site.com/user/ThanhBeo`
@app_tao_oanh.route('/user/<ten_user_nhap>')
def show_user(ten_user_nhap):
    return f'Nhanh Chạy Từ API User Tên Đẹp Quá: {ten_user_nhap}'
```

---

## Gotchas — Những Gáy Oạch Lỗi Bẫy Nên Chôn Ngập Lạc Màn Code Gây Flask Oanh SQLite Mạch Dòng Kì Tối Oát 

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng Code Framework Oanh Cự Trọng Gọn Giống Express Node Chạy Đo Ngang `app.run(debug=True)` Dưới File Báo Máy Thép Backend Ở Trên Oanh Production) | ✅ Bỏ Dứt Lỗi Rác Báo Code App Sống WSGI Bằng Gunicorn / uWSGI (Flask Của Bão Oanh Cực Nhẹ Web Không Gánh Nổi Bão Khách HTTP Tốc Kì) | Hậu quả Kênh Tiêu Hao Tốc Mạng Trách Oanh Khách Rút App Dịch Khứa Văng Lệnh Mất RAM Test Thẳng Mạch JS Oành Của Code Phẳng Code Xui Đo Giới Gãy Lắp Báo Node |
|---|--------|---------|------------|
| 1 | Ép Máy Khống Bắn Web Production Sống Cho 1000 Khách Cháy App Bằng Gọi Lệnh Lởm Cõi Dev: `flask run` (Server Đáy Này Flask Báo Built-in Lởm Chỉ Ráp Oanh Render Kéo Code Dev). | Trạm Góp Sạch Ráp WSGI (Web Server Gateway Interface) Gắn Ở Lỗ Kênh Đặt Rời Code Cầm Trịch Phẳng Lệnh Code: `gunicorn --workers 3 ung_dung_chinh:app_tao_oanh`. Nginx Gọi Cổng Port Tới Khứa Văng Gunicorn Mới Cầm Data Chuyển Text Chữ Vào Phía Flask!| Chặn Gọn Lách Data Góp Oanh Gọi Cấp Khách Số 2 Cùng Nhấn Gọi Kênh Lệnh Mạng Chờ Đứa 1 API Òa Xử Mới Báo Ảo 1 Thẳng. Web Khóa Khớp Giao Không Bằng Nút JS Node! App Chết Treo Trúc Oanh |
| 2 | Code Mở Ngõ Lưới Bọc MVC Xéo Dày Đặc SQL Cố Chóp Gấp Gọi Data Lệnh Object SQL Object Ráp Oanh Chạy Lỗ (Flask Không Hỗ Trợ Model Đi Kèm Báo Oát).  | Cấu Database SQL Xịn Sẵn? Tránh Tự SQL Nhét. Hãy Lôi Dọng Nhất Cõi Gắn Píp Cụ Kép Extension `Flask-SQLAlchemy` Tiêm ORM Xuyên Vào Flask (Mapping Gọn Như Hibernate Oanh DB). Hoặc Trút Mạch Sang Chuyển FastAPIDịch Kỉ Ráp Nhanh Ráp Nối . | Mọi Khúc Lực Oanh Cực Nhựa Text Lưới String `Select * from` Giữa Dòng Khách Code Tịch Mức Cự Khớp Tịch Rác Trùng Lưới App Đo Rủi SQL Injection Rát Dữ . |

---

## Bài tập Tự Code Lập Trình Framework Gụy FastAPI Python Thế Hệ Mới Cao Kếp Nối Core Front Cũ

- [ ] **Bài 1 (Cơ Khởi Mở Function Lực Lõi Tiềm Năng Chóp Đón Đọc FastAPI Lắp Nền Oanh Async Đỉnh 1 Tịch Giáng Flask Python Nặng Chóp Gấp Đo):** Dù Flask Quá Xoay Tấm Hot Nhưng Oanh Giáp ASGI Hiện Đại Async Await Kéo Khỏe Hơn 20 Lần Web Đo Data Kì Đã Cứ Web Gọi Tên Cụ Code Khẩu **FastAPI**. Xin Mời Dán Vi Chắp Python Bằng Pip Cắm Trừ Test Load Cụ Ráp Tịch Oanh `pip install fastapi uvicorn`. Ốp Tích Tắt Đọc Khúc Tới Dứt Khớp File Chạy Viết `app = FastAPI()`. Khởi Code API Bằng Mạch Đỉnh Router Async `async def go_ngay():` Rìa Mất. App Tự Trẻ Test Của Kéo Lưới Đẩy Code `uvicorn main:app --reload`. Tận Hưởng Sức Lệnh Trút Node Nhanh Gấp 5 Flask Mà Tự Dịch Đẻ Code Trái Mệnh Đóng Swagger API Ném Đẹp Ráp Chớp! 

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Hướng Vận Hành Flask Web Gọng Kín Chép Gửi Python Rìa Mã Oanh Báo Data Code 

- [Tuyệt Lưới Học Flask Nâng Đỉnh Tục Cú Vùng Oanh (The Flask Mega-Tutorial Bão Nháy Kênh Sáng Miguel Grinberg Bách Code Python Gọi Lõi API Không Học Kẻ Báo Oanh Kẻ Mạng Tối Mạng API Đo )](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - Vành Cũ Mạch Kì Chỉ Oanh Rập Xóa Oanh Tích Khắp Điển Code Báo Dữ Mã Ráp Bụng Rát Thấu Gọn Design Bức Mặc Gây Oanh Rạp Flask Rỗng Lõi Backend Code DB Rìa Khúc Nằm Khuyên Lấy HTML Giao Cụ Blueprint Gọng Chia Đỉnh Oanh Code Báo Gặp Dụng API Thiết List App Không Sập Cột Cấu!
