# Hướng Dẫn Xử Lý Lỗi: "command not found: python"

Đây là lỗi phổ biến nhất khi người dùng chuyển từ Windows/Linux cũ sang macOS hiện đại.

## 1. Dấu hiệu nhận biết
Khi bạn gõ lệnh chạy ứng dụng:
```bash
python app.py
```
Hệ thống báo lỗi ngay lập tức:
```text
zsh: command not found: python
```

## 2. Nguyên nhân
- Trước đây, macOS cài sẵn Python 2.7 và lệnh gọi nó là `python`.
- Từ các phiên bản macOS gần đây (Monterey, Ventura, Sonoma...), Apple đã **loại bỏ hoàn toàn Python 2**.
- macOS có sẵn Python 3 (đi kèm Xcode Tools), nhưng lệnh gọi của nó mặc định là `python3`, **không phải** là `python`.

## 3. Cách Kiểm Tra (Diagnosis)
Để xác nhận máy bạn đang có những gì, hãy chạy các lệnh sau trong Terminal:

```bash
# Kiểm tra lệnh python cũ
which python
# Kết quả: "python not found" (trống trơn)

# Kiểm tra lệnh python3
which python3
# Kết quả: /usr/bin/python3 (Có tồn tại)
```

## 4. Giải Pháp

### Cách 1: Sử dụng lệnh `python3` (Khuyên dùng)
Đây là cách rõ ràng và chuẩn nhất. Thay vì gõ `python`, hãy luôn gõ `python3`.
```bash
python3 app.py
pip3 install flask
```

### Cách 2: Tạo Alias (Nếu bạn quen tay gõ python)
Bạn có thể "đánh lừa" thói quen bằng cách bảo máy tính rằng "khi tôi gõ python, hãy hiểu là python3".

1. Mở file cấu hình shell (zshrc):
   ```bash
   nano ~/.zshrc
   ```
2. Thêm dòng này vào cuối file:
   ```bash
   alias python="python3"
   alias pip="pip3"
   ```
3. Lưu file (Ctrl+O -> Enter) và thoát (Ctrl+X).
4. Cập nhật cấu hình:
   ```bash
   source ~/.zshrc
   ```
Sau bước này, bạn có thể gõ `python app.py` bình thường.
