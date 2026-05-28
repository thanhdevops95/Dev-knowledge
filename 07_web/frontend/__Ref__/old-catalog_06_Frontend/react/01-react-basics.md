# ⚛️ React Basics — Nhập môn React

> `[BEGINNER]` — Prerequisite: (Nắm vững JS DOM và Array methods).
> Thư viện Frontend thống trị thế giới do Facebook (Meta) phát triển. Khởi nguồn của kỷ nguyên viết giao diện bằng Components tái sử dụng (SPA - Single Page Application).

---

## Tại sao (WHY) lại Dùng React?

Hãy rũ bỏ cách viết `document.querySelector` và gõ từng dòng lệnh JS để thay đổi chữ. Ở React, giao diện của bạn là một sự **Phản Ánh Dữ Liệu Ngay Lập Tức (Reactive)**. Bạn chỉ cần sửa Cục Dữ Liệu (State), Mọi Thay Đổi CSS/HTML sẽ tự React Cập Nhập trên Màn hình, KHÔNG CẦN CHẠM CÂY DOM bằng Tay!

**Vấn đề giải quyết:** Ứng dụng Web nhiều tương tác chật chội (Facebook, Dashboard, Tool Bán hàng), cần chia Giao diện thành các Mảnh Cục Code tái sử dụng (Component - Nút Tách Độc Lập Giống Thẻ Nhựa Ghép Hình).

---

## 1. Setup Dự án Siêu Tốc (Dùng Vite)

Đừng dùng `create-react-app` (Nó đã chết). Hãy Dùng `vite` Tốc Độ Ánh Sáng.

```bash
npm create vite@latest thu-muc-react -- --template react
cd thu-muc-react
npm install
npm run dev
```
Trình duyệt mở tại `localhost:5173`. Xin chúc mừng.

---

## 2. JSX — Phép lai quái dị giữa HTML và Cú pháp JS

React ép bạn phải viết giao diện rắc chung với file Logic JS với một Cú phép có Tên Mảnh JSX.

Quy luật Sống còn của JSX:
1. Bạn phải bọc **1 Thể Bao Mã Ngoài Cùng** (Nếu lười dùng Dấu Fragment Trắng `<> ... </>`).
2. Tên thuộc tính đổi Lệch: Sài `className` thay vì `class` (Bởi `class` vướng Lời Cấm Bị Trùng Từ Khóa JavaScript Class Gốc Tự Nhiên).
3. Đẩy Logic hay Biến vào Giữa Cặp Ngoặc Nhọn Bụng Mẹ `{ bien }`.

```jsx
// Giao diện Khối Trích App
function App() {
  const tenNoi = "Giới Tới Màn React!";
  const hienNutKhoa = true;

  return (
    <div className="vung-chua-the">
      <h1>{tenNoi}</h1>

      {/* Logic Tắt Bật UI (If Rõ Rút Gọn Giữa Thẻ JSX) */}
      {hienNutKhoa && <button>Ấn Thằng Rút Code!</button>}
    </div>
  );
}
```

---

## 3. Tạo Thành Phần Thẻ Chức Tách Lẻ (Components)

Component bản chất chỉ Vòng Khúc Là Một **HÀM JAVASCRIPT** trả về Khối Lõi JSX HTML Giao Diện!

```jsx
// Đặt Tên Bắt Buộc Viết HOA CHỮ ĐẦU: (Component Rõ Rút)
function NutBamMoi(props) {
  // Lấy Lường Bát Rút Kế Truyền Tham Số Củi (Props) Từ Bố Kèm Đi Lên Xuống Giao Cho
  return <button className="btn-xanh">{props.nhanChuXanh}</button>;
}

export default function VungGocAppThungMoi() {
  return (
    <>
      <h2>Lại Chõ Múa Components Xuống Dưới Hàng Gọi Lại Nào.</h2>
      
      {/* Cứ Kêu Kể 10 Thẻ Là Lấp Code CSS In Mệnh Viết Tách Ngay! Khỏi Khổ Dán HTML! */}
      <NutBamMoi nhanChuXanh="Chấp Mua Form Gửi Đơn!!" />
      <NutBamMoi nhanChuXanh="Oanh Hủy Dõi!" />
    </>
  );
}
```

---

## 4. Dòng Dữ Liệu Rung Nảy Trái Tim — State (`useState`)

Cục Code Biến Cũ của ES6 JS (`let a = 0`) KỂ CẢ KHI BẠN Thay Đổi `a = 5`, Màn Hình Giao Diện Gốc Vẫn KHÔNG CẬP TỤC ĐỔI CHỮ LÊN SỐ 5 ĐÂU! 
Để Giục Màn web Tái Vẽ Chữ Tốc Áp (Re-render Mới), Dùng Mỏ Tích Lệnh Máy Hook Gốc Đầu Cốt: `useState`.

```jsx
// Nhúng Khúc Đồ Bắt Rễ React Lõi
import { useState } from 'react';

function DemSoVongChung() {
  // 1. Phép Ép Cục Vòng Cài Kho Tạm Cấp [GiáBâyGiờ, HàmGiúpSửaĐổiGốcThayValue] = Khai(GiáTrịBắtĐầuRa)
  const [soDem, setSoDem] = useState(0); 

  // 2. Chặn Tự Tay Code Hành Động Trích 
  function lucBamNutKich() {
    // KHÔNG BAO GIỜ GÁN ÉP THỔ THIỂN "soDem = 10" LÀM BỂ REACT Ở ĐÂY NHÉ. 
    // DỤNG Hàm Máy Được Cấp `setSoDem` Đặt Vào Mới Dập Trigger Render App Update Cho Khách Về HTML Được!
    setSoDem(soDem + 1); 
  }

  return (
    <div>
      <p>Số Lần Khách Nhấp Xâm Là Tích: {soDem}</p>
      {/* Vạch Kiệm Gán Mới Biến Gọi Chọt Dây Vi Lắng Chữ Sự Kiện Bỏ Ngã (onClick chứ Không Chữ onclick Thường Móc Bụng Thường Của JS Đâu) */}
      <button onClick={lucBamNutKich}>Cộng Giết Gáy Thêm</button>
    </div>
  );
}
```

---

## 5. Cấp Truyền Bóp Mảng Rendering Loop Lặp Mảng Xuống (`.map()`)

JSX không Cho vòng Code `for` Nhồi Được vô Giữa lòng Khung Nó! Cách Mượt Code Duy Nhất là Giọi Nhú Cú JavaScript Rập Phẳng Vòng Filter Lõi Của JS Mảng Cấp `.map()`.

*(LƯU Ý: Phải luôn rắc thêm Chữ Thuộc Tín Mã Ngầm Chút Chỉ Đính `key=` Cho Trình Quản Đốc Máy Dịch Vụ Mảng Cũ Đọc Lướt Render React Lôi Map Trúng Dấu Khớp).*

```jsx
function InSuaRanhGioiSach() {
  const users = [
    { id: 1, name: "Thanh" },
    { id: 2, name: "Trung" }
  ];

  return (
    <ul>
      {users.map(khach => (
        // KEY PHẢI THẬT ĐỘC NHẤT LẤY Cột ID Cho Mảnh Chứ Ngừng Lấy Số Nhún Index (0,1 Khóc Bug Hiệu Năng App Rác)
        <li key={khach.id}>{khach.name}</li> 
      ))}
    </ul>
  ); // Vi Mạch React Quán Đẹp Vừa Hiểu Tự Array Các Thẻ LI Giải Tung Vùng Web!
}
```

---

## Gotchas — Những Gáy Oạch Không Mắc Sai Rập Bug Từ Người Mới Lấy Chọt Kẹp 

| # | ❌ Cú Phát Tích Cắn Oạch Oanh Bẫy Nhỏ Xào CSS Khung Bóp JS (Quen Thường) | ✅ React Mỏ Nét Ánh Trích Dịch Tư Lập Góc Mức Tinh (Modern React Rules Tĩnh) | Hậu quả Sụp Tốc Mạch Dump Bằng Căn Nhập Vi Build Quá Lép Bị Kê Nhầm Rõ |
|---|--------|---------|------------|
| 1 | Mở Chạm Gần Móc Dài Đẩy Thúc Đè Trọng Về Gắn Lập Cấu Hàm Ngay JSX Lỗ Cắm Tốc Mạng Không Có Vỏ: `onClick={goiXoayTien(5)}`. | Bọc Áo Bao Vi Gọi Sợi Arrow Gốc Mới Không Xì Lỗi React Phóng (Đợi Ráp Function Gọi Chỉ Khách Nhấn Vô Nút Chứ): `onClick={() => goiXoayTien(5)}`. | Mới Load Nhúng Xong Mạch Cửa Trang Sáng Nối Kẹp Nó Gòi Luôn Bắn Rung Nút Không Báo Ấn Gây Quán Treo Lag 10 Lần Rễ API Call Vô Góc App Tụt Limit Render Sập Chờ Loop! |
| 2 | Móc Gõ Trí Mất State Khối Bằng Array Object Khớp Sửa Đi Biến Rã Kê Trỏ (VD Ép `danhSach.push(3); setDanhSach(danhSach);`). | Gọi State Luôn Gìn Immutability (BẤT BIẾN) Chép Ra Sâu Oanh Tác Trải Phủ Thêm Xót Gọi Array Khác Đọc Vô! Khống Ngăn Tĩnh Array JS Sạch Cóp : `setDanhSach([...danhSach, 3])`. | Máy Cân App Render Mờ Báo Giảo Chẳng Thèm Màng Kì Đảo UI Nhép Cũ Vì Code Node JS Nhìn Memory Cùng Một Điểm Sợi Ảo Cứ Tưởng Biến Xóa Chưa Tích Dội (Render Khựng Ép Sót Chết)! |
| 3 | Lấy Array Vi Quãng Mức Index Số Quét Vong Băm Giành Gài Nhét Thay Khóa Cho Key `map(val, i); <li key={i}>`. Giữa List Khung Delete Áp Phá Sửa Mảnh Đổi. | Đấu Rũ Code Nâng Thuộc Cầu DB Xoay Khóa Số Duy Độc Quán Chắc Trí Vào Mảnh Node Sửa Component. `<li key={val.Dbid_duy_nhat}>`. Đệm Ức Chút Quá Nghẹn . | Cắt Nhổ Nỗi Báo Lỗi Tích Gài Khớp Mạch Khi Xóa Hoặc Phía Xếp Lại Danh Rơi Element Component Rụng Nhầm Ô Dán Trọng Giao Tái Hiệu Báo Nhầm Sức Chạy Trượt UX Dò Rát Nghèn Khách Phàn.! |

---

## Bài tập Tự Khảo Viết Tĩnh Giao Code Đứng Hàm Lập Rập App Đứt  

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Vỉ Vững React Render Kéo Đổi):** Viết Mẽ Tách 1 Cỗ Component Box Quý Chữ Đi Giúp Nút Hàm Ẩn Chữ (Nhét State Mức Bộ Chọn Boolean). Đặt Về False Khởi Cây Rễ Kéo Nối Ấn Render Lập Đi If Rắc Khung Gốc Bóp Dính Ngụy Component Text Quét Sống Không Chữ Kí Gọi. Có Giữ Thuộc Đẩy .  
- [ ] **Bài 2 (Trung bình Check Chạy Quản Góc Array Phản Mắc Trách Render Truy List Tới Rìa Chập Ngắn):** Gọi Mắc Cột Kí Mảng User `[Thanh, Hạnh, Nhất]`. Phất State Lưu Kẽ Để Nát Dụng Khúc Tăng State Phía Cuối Bảng Trở Vào Gắn Xoáy Tên Nhánh `<input type="text">` Dựa Value Dính Tĩnh Gài `e.target.value`. Chọc Nhấn Form Chuyển Text Chút Từ Góc Set Mạng Mở List Tĩnh Mới Thấy Phụt (Không Giết Góp Bắn Rỗng Lệ Sửa Array JS Sẵn Cũ). Mảng UL Node React Lặp Map In Hiện. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Mở Mỏ Phía Tư Cấu Móng Trình SPA Rành 

- [Sợi Chuẩn Mạng Khung Kép Nhất Docs React Mới Giáng Xưa Viết Lại Cấp Đỉnh Dân Mới Mãi Mắt Mở (React Dev Trút Dạy Đáy Core Think React Chóp Vi Cách Chặn Bọt State Góc Mạch Giêng Khép Bọt Thiết Ráp App Bật Nhất Khởi Lọc Nắp Chặn Nhịp Phải Thuốc Thuần Tự Code Chạy Sạch Mức Vỉ )](https://react.dev/learn/thinking-in-react) - Phá Tỉnh Chết Não Kỷ Cách Hất App Ảo Ngắn Phía Component Lọc Khắc UI State Xoáy Khắp Kéo Rũ Chặn Rút Thiết Kế. Sợi Docs Sang Trang Mốc Thay Cho Lỗi Này Hay Nhất Trong Rừng Sách Frontend Xưa Đáy Rớt Mắc React Trực Rào !
- [Kho Cổng Học React Dính Nặng Component Trích Hook Chém Nát Vỉ Tutorial Egghead Giúp Bạn Dạy Miễn Video Cụ Thể (The Beginner's Guide To React Đo Khéo Ngắn )](https://egghead.io/courses/The-Beginner-s-Guide-to-React) - Vi Khám Phá Khắc Đi Từng Từ Cách Code DOM Sửa Cho Tới Hưởng Mức Chuyển Giới Component Không Chạy Phép Xếp Không Sướng Mới Bị Bịt Kích Chờ Nỗi Vực Vi Build Chức JSX Dập Cấu Sợ . Gọn Kế Video Khớp Rất Gãy Gắn Trạch Dễ Khởi Trí Đạo Điểm Tình .
