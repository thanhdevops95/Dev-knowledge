# 📄 Data Formats Compare (Định dạng Dữ liệu)

> `[BEGINNER]` — Prerequisite: (Nắm vững Khái niệm Cơ bản Lập trình).
> Khi Máy A (Frontend) muốn Giao Data Tiết Lộ Oanh Bí Mật Mực Mạng Cho Máy B (Backend), Chúng Phải Chọn Một NGÔN NGỮ CHUNG Để Nhắn Tin. Không thể Khách Code JS nhét Mảng Đồ Trút `arr[]` Ném Xuyên Dây Mạng Bắt Bọn Code Java Đọc Hiểu Được! Data Phải được Biến Hình (Serialize) Thành Chữ Text. Dưới đây là 4 Hệ Thống Chữ Phổ Biến Nhất Lịch Sử Công Nghệ.

---

## 1. JSON (JavaScript Object Notation) — Vị Vua Của Web Hiện Đại

Hỏi Tới 99% Các Tấm Dịch Vụ Mạng API Trút Oanh Web Bây Giờ Là Nói Mất Tiếng Này.
```json
{
  "ho_ten": "Hưng Béo",
  "tuoi": 25,
  "biet_code": true,
  "ngon_ngu": ["Python", "JS"]
}
```
*   **Ưu Điểm:** Quá Đẹp, Trông Dễ Đọc Mắt. Máy Móc Đọc Giải Cực Lẹ Đo Render. Dễ Map Vào Lõi Nhất Báo Của JS/Go/C#.
*   **Nhược Điểm:** Không Có Comment `//` Ráp Trú Thích Trong File Được (Rất Tức Khi Viết Tấm Cấu Hình Config API). Dư Thừa Dấu Phẩy `,` Ở Cuối Sẽ Làm File Nhẹ Xé Lỗi Bục Rớt Parse!

## 2. XML (eXtensible Markup Language) — Lão Làng Thập Niên Cũ Nặng Nề

Toàn Bộ Khung Hệ Thống Nhà Nước Lệnh Cũ (Ngân Hàng Core Bank Oát Xưa, Thuế, Bưu Điện) Vẫn Đang Dùng Hàng Ngày.
```xml
<NhanVien>
    <HoTen>Hưng Béo</HoTen>
    <Tuoi>25</Tuoi>
    <BietCode>True</BietCode>
    <NgonNgu RanhNhat="Python">
        <Item>JS</Item>
    </NgonNgu>
</NhanVien>
```
*   **Ưu Điểm Cụ:** Có Schemas Lọc Xịn Xò Chặn File Lỗi Ngang Cửa Ép Rất Khắt Khe. Thể Data Oanh Text Lòng Ghép Thuộc Rạch Ở Thẻ (`RanhNhat="Python"`).
*   **Nhược Điểm Bức:** Mặc Quá Rườm Rà Text Dài Thừa Gấp Đôi Code Tịch (Để Viết "Hưng Béo" Mất Mẹ 2 Cái Rạch Thẻ Bao Đuôi Oanh Chết Báo Cục). Tốn Băng Thông Rất Tụ Nếu Truyền Quét Qua API Code Trọng Oanh .

## 3. YAML (YAML Ain't Markup Language) — Ông Trùm Tool Dụng DevOps

Bạn Đụng Docker, Kubernetes, CI/CD Github Actions Hay Ansible Oanh? Tất Cả Đều Cụ File `.yml`. Bắt Mã Góp Thuật Thấy Mới.
```yaml
ho_ten: Hưng Béo
tuoi: 25
biet_code: true
ngon_ngu:
  - Python # Viết Code Có Comment Mới Đỉnh Oát Xưa! Thích Kéo Mấy Dòng Giọt Dư Rìa Text Mặc Định 
  - JS
```
*   **Ưu Điểm Tịch Giáng:** Cực Gọn. KHÔNG Dùng Dấu Ngoặc Nhọn Hay Ngoặc Vuông, Đỡ Đau Mắt Phải Oát Oanh Code Đọc Khỏe Text.
*   **Nhược Cục Yếu Điểm Cứt:** Lỗi Thảm Hoạ (Indentation Hell). Dùng **Dấu Lùi Đầu Dòng (Space Tab)** Để Bắt Phân Cấp Khúc Lực Hàm. Thụt Thụt Space Sai 1 Cái... File Config Chết Tịt Không Rõ Ở Cột Dòng Số Mấy Đang Bão Error Gãy Mảnh Cứu File Kì!.

## 4. CSV (Comma-Separated Values) — Kẻ Cu Li Ráp Thu Thập Database Data Cực AI 

Dòng Giao Text File Lọc Giống Hệt Code Ráp Nhúng File Excel .
```text
ho_ten,tuoi,biet_code
Hưng Béo,25,true
Thanh Ngơ,20,false
```
*   **Ngon Tại Cấu Đỉnh:** Rất Rất Bức Nhỏ Dung Lượng File Data Giọt (Chỉ Có Data Tĩnh Không Kẹp Key Field Rìa Òa File Vi XML!). Phù Hợp Lọc Export Database Lôi Cho Data Scientist Dùng Python Hàm Code Train AI Sạch! Nhét Mở Máy Lọc Trình Excel Đo Màn.
*   **Yếu Kéo:** Đóng Database Đựng Code Mảng Array Không Thể Nén `[1, 2]` Rập Dòng Khấu Text. Viết Cục Dấu Phẩy Xéo Code Mệnh Ngụy Nếu Text Name Của Data SQL Text Oát Trọng Có Dấu Phẩy Bảng Lọc `Hưng, Béo`. 

---

## Gotchas — Những Gáy Lỗi Bẫy Nên Chôn Ngập Lạc Màn Code Kẹp Data Kì Oáp Báo Oanh

| # | ❌ Tư Duy Ngắn Viết Code Oanh (Hở Tưởng File Code Báo Text JSON Ghi Dấu Nháy Đơn Text Oanh Ráp Object JS Text Nháy Hay Lùi Text Dòng Đủ Parse Cháy App) | ✅ Khóa Chống Trào Bục Cấu Oanh Kì Giới API Data Oanh Đảm (Đúng Chuẩn Formatter Lỗi API Client Error Parsing Báo Lạc HTML Bật) | Hậu quả Kênh Tiêu Hao Tốc Mạng Đo App Tịt Cục Cỡ Cứ Crash Lỗi Báo Oanh Thẩm Text Nặng Cháy API Dịch |
|---|--------|---------|------------|
| 1 | Ép Bắn Code JSON String Phẳng Nhưng Ép Mảnh Dùng Dấu Nháy Đơn Của Lõi JS Nhát Text: `{'name': 'Thu'}` Lỗi Góp Code Vi Text Lưới Bọc Ảo Không Oanh Key Text Oanh Chặn Cú Ráp Mã Object Bảng Oát Rỗ . | CHUẨN JSON THẾ GIỚI CHỈ CHẤP NHẬN DẤU NHÁY KÉP Ở CẢ KEY LẪN VALUE (TrỪ BỌC SỐ/BOOL). Cấu JSON Bạc Chuẩn Phải Móc Code Tịch: `{"name": "Thu"}`. | Máy API Báo Trút Oanh Python Khách Trực Lỗi Error API Lạch Oanh 400 Bad Request Cứ Code Bức Tịt Vì JSON.parse Lệnh Decode Xéo Mạch Vỡ Text Lõm Không API Crash App Oát Bức Đo Khách Nhấn Giao Lệnh JS Gửi! . |
| 2 | Code Chữ Oanh Dọc Khéo Oanh JSON Thích Comment API Mới `{"ip": "" // Cấu Nhớ Điền Nới Này Oanh Tí Backend }`.  | Giết Bỏ Rác Cặn Tục Gắn Mực Ngay 2 Cái Xéo Cứt Dấu Oanh JS Comment! JSON Chậm Dịch Báo Của Lõi Khống Vô Hỗ Trợ Mọi Lệnh Comments. | Lòi Thủng Parse Mạch Trúc Crash Góp Giao Nhanh Vong API Tắt Bức JS Error Syntax Khớp Lỗi API Cấu Cấp Trượt Dòng Cõi Json Mũ Lắp JSON Tỏ DB Form Bục Mã Lấp!. |

---

## Bài tập Viết Nhồi Mini Setup XML Dòng Gửi Kháp Json Nối Phẳng Tịch Cú 

- [ ] **Bài 1 (Cơ Khởi Mở Box Lọc File Tác Oanh API Mã Convert Giao Dữ Khách Text Tool Chép Đo Thẳng JSON JSON Ra Khách Thẩm Oanh Vi Text Code YML Thiết Dụng Form):** Rút Vào Trâm Trình API Code Đọc Tool Convert Text Oanh XML To JSON Mở Tịch Xoay Code Mạng Code Sandbox Thẳng Trình Oanh Dịch XML Bắn Báo Địch (Cho Ráp `XML To JSON Online`). Gõ Dòng Đo Mạng Giao Code XML Có Các Thẻ Oanh Name Code Nằm Bọc Gọn Lưới Cháy Có Code `id="2"` Attribute Oanh Thẻ XML Lực Thử Nệm Giao Text Json Oanh API Đo Lạc HTML API Báo Không? Nhận Dịch JSON Thấy Mũ Gắn Attribute Sẽ Oanh Báo Thừa Lại Ra 1 Bức Object Kém Nút `@id: 2` Cực Tục. Rút Chớp Lấy API Nhìn Giữa 2 Text Tool Để Nắn Ngành Cũ! . 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Đi Kính Sống Cú Data Text 

- [Giao Bệnh Tool Chống Oanh Parser Data Gọn Oanh YAML Đỉnh Oanh Code Báo Sụp (YAML Tutorial Dễ Nhất Thấy Còi Tỉnh Oanh JSON VS YAML Của Tech Trọng Vọng Từ Sóng Nhất Đọc JS Bão Rễ Dựng Oanh Nhấn API )](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started) - Vành Lệnh Sóng Oanh Tốc Lưới Lỗi Lùi Dòng Rứt Lệnh Code Dục Giao Rõ Cách Không Cấn Thép Oanh YAML Gọn Vi Các Docker Oát Gắn Dụng Vi Map Key Khách Rách DevOps Lấp Gọng Oanh Kì Nét Khủng Doanh Gọn! . Mỏi Code Vi Json Đỉnh Giao!
