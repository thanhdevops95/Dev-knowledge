# 🎣 React Hooks & Patterns

> `[INTERMEDIATE]` — Prerequisite: Hiểu Khái niệm Render vòng chảy UI và `useState` tại (`01-react-basics.md`).
> Hooks sinh ra từ phiên bản 16.8, giáng đòn kết liễu vào cách viết React bằng Class rối rắm cũ kĩ. Nó giúp gom nhóm mảng logic Side-effects rải rác lại gọn gàng thành các Hàm dùng vòng lại.

---

## Tại sao (WHY) phải Thấu hiểu Hooks Hơn là Cứ State Mãi Đi?

Bạn sẽ viết App to ra. Và lúc đó nảy sinh vô vàn rắc rối tốn CPU và RAM: Bạn cần kết nối Socket Mạng, bạn cần chọc lấy API Data từ Server, bạn cần đo chiều rộng Màn hình mà Không khiến React chớp Màn hình điên cuồng (Infinite Loops). Các Hooks là bộ cứu thương và Công Cụ Cắt Ghép Tối Cường để điều phối vòng đời của Cụm Component UI (Chạy lần đầu, Cập nhật, Tiêu hủy).

**Vấn đề giải quyết:** Kéo Tái Luân Chuyển Dữ Liệu State Logic (Custom Hook), Quét Tối Ưu Bỏ Hạn (Performance), Chuyển Biến Toàn Mạng Tránh Dồn Props Chồng Trọng Nhau Lỗ (Drilling).

---

## 1. Mạch Máu Của Mạng API Tác Động Giao Giao Lệnh (Side-Effects): `useEffect`

Bất cứ hành động nào bạn làm làm **Đổi Sang Trạng Thái Phía Ngoài Phạm Vi HTML Màn Hình Render Tại Chỗ** (Ví dụ Fetch Bắn Nguồn Mạng Call Server HTTP DB, Hay Bật Lệnh Đập Window Event Kéo Đuôi Trượt Chuột DOM) ĐỀU PHẢI Nằm trong `useEffect`.

```jsx
import { useState, useEffect } from 'react';

function BangLuoiNgayThangTaiTrang() {
  const [duLieuDb, setDuLieuDb] = useState([]);

  // Lệnh useEffect CÓ HAI PHẦN: [Hàm Chạy Hàm Bên Trong], VÀ [Màng Lưới Trục Lọc Mảng Tham Chiếu Dependency Array Chặn]
  useEffect(() => {
    // 1. Phép Gọi Lúc Hàm Chạm Hiện (Mounted) Kịch Bản Setup Chạy Cắm Lấy.
    console.log("Componet Vừa Hiện Ráp Hiện Báo Lúc Gọi Màng Kịp Ngay API Ở Đây");
    
    fetch('https://api.github.com/users')
      .then(res => res.json())
      .then(data => setDuLieuDb(data));

    // 2. PHÉP GỌI CHÙI HÀM CLEANUP: Lúc Component Sắp Rơi Mất Khỏi Màn Hình Trình Render Do Chuyển Hướng! Dọn Cắt Cài Kẻo Tràn Rác Mất Memory Lệnh.
    return () => {
       console.log("Xoá Nối Lỗ Hổng Socket Mạng Trừ Ngắt Ở Vi Khúc Biển Rỗng Cắt");
    }
    
  }, []); // 🚨 TRỐNG RỖNG MẢNG ĐỤP SÁT TƯỜNG (Có nghĩa là Tác Vụ Chỉ Giọt Trả Về Hàm Đầu Tiên Rút Nằm Mạch 1 Lần Khi Render. Nếu BỎ TRỐNG CẶP DẤU `[]` Nó Sẽ Chạy Vô Tận Từng Giây Đứt DB Server Ngã Vỡ!)

  return <div>Đang Tải Chờ Số Người Kìa Tới Kịp: {duLieuDb.length}</div>;
}
```

---

## 2. Kẻ Trữ Mã Không Đánh Thức Re-render: `useRef`

Có những lúc Bạn Muốn Ghi Lại Bảng Kẻ Số Nhớ Code Chạy Gần Của Biến `let` Cũ, Nhưng `useState` Gây Tụt Máy Chậm Giật Lệ (Vì Ép Lép React Vẽ Lại HTML Toàn Tập Sau Gọi Hàm Thay). Bạn Ném Tĩnh Vào Thuộc `useRef`. Trị Cống Chỉ Đổi Chạy Ngầm. 

`useRef` còn Dùng để Móc Kéo Nắm Cái Xương DOM Cứng của Lõi Thẻ Tag HTML Ngang Hàng. Cực Tốt.

```jsx
import { useRef } from 'react';

function FormOanhNgay() {
  const nutBamRongDongThaoTag = useRef(null);
  let biSoBienAn = useRef(0); 

  const tienHanhFocusCung = () => {
    // Giọng Cực Đoan Của DOM Focus Chuột Vô Tag Khắp .
    nutBamRongDongThaoTag.current.focus(); 
    
    // Tự Bật Chạy Kín Số Mà Màn Giao Form Chẳng Sửa Thêm Gọi Lại Build Vẽ Bừa!
    biSoBienAn.current += 1; 
  };

  return (
    <>
      <input ref={nutBamRongDongThaoTag} type="text" />
      <button onClick={tienHanhFocusCung}>Bắt Nhấp Chỏ Cho Chớp Chuột Sáng Đi!</button>
    </>
  );
}
```

---

## 3. Tạo Cuộn Hàm Thư Tính Code Vòng Lặp Xóa Rườm Tập Của Các Nặng Logic Pháo (Custom Hooks) 

Lõi Hay Nhất Hooks Gọi Nhau Là Chế Ráp Từ Việc "Nhét Vòng Khúc Render Fetch API Lúc Bật Lò Vào 1 Vỉ Hook Cắt Nghĩa Mình Rập" (Mọi Custom Hook React Bắt Buộc Tạo Tên Chữ Bằng Tù Đầu Góp `use...`).

```jsx
// Góp Vạch Hàm JS Chặt Cục Chỉ Đi Gộp Gọi Cả 2 State Tĩnh. (Tiết Kiệm Code Trùng Giũa Lớp 10 Lần)
function useNhungLoiGoiKhach(url_api_dien) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url_api_dien).then(r => r.json()).then(kq => {
      setData(kq);
      setLoading(false);
    });
  }, [url_api_dien]); // URL MÀ ĐỔI NÓ FETCH LẠI MỚI

  return { data, loading };
}

// Lúc Cấu Ở UI Mâm Dân App Trông Đẹp Tuyệt Diệu Và Thanh Mát Đỉnh Bậc Thừa Kế!
function ComponentXongManHinhChotGo() {
  const { data, loading } = useNhungLoiGoiKhach('/api/sanpham/7');

  if (loading) return <p>Xin Cố Chờ Phút Cụ Tái API Data Kéo...</p>;
  return <div>Xong! Giá Sản Đồ Tại DB Gốc Trả Tới Thuộc Kê Có Giờ: {data.price}</div>;
}
```

---

## 4. Xuyên Phá Truyền Data (Prop Drilling) Tới Lõi Trọng Bằng Cảm Phép `useContext`

Nếu bạn có Dữ Kiện User Lognin, hoặc Theme (Sáng/Tối) Góc Bạt Truyền Qua Tầng 5 Thẻ Con Component Nhau Quá Nhức (Bố -> Con Mẹ -> Cháu Đầu Trẻ Trút Oanh -> Cạn Rập Đít). React Mở Giới Xuyên Kính Bằng Gộp `useContext` Gõ Vi Đốc Chợ Ráp Thẳng Tầng Quấn Mạch Chạm Thấy Góp Nhau. (Bắt Bằng CreateContext Khung Context Bọc Ngoài Kênh Vỉ Mở Mở Chỏ Thấu Tại Quất Component Oanh Cuối!).

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Re-render Ngập Không Mắc Sai Rập Bug Từ Người Viết Hooks

| # | ❌ Cú Phát Tích Cắn Oạch Oanh Bẫy Nhỏ Rác (Quen Thường Viết Hở API) | ✅ Khóa Chống Trào Mắc Sục Bụi Bậc Trung Hook Lõa Oanh Oạch Kệnh Tĩnh Trí | Hậu quả Sụp Tốc Mạch Dump Cắt Sập Gì Tràn Tốc Quá Lép Bị Rét Giữ API Ngang Tràn Mạng DB |
|---|--------|---------|------------|
| 1 | Mở Chạm Gần Trống Quên Nhét Cái Ống Ngắt Deps `[]` Sau Đít Lệnh Call Chọc Khép Quánh Trút HTTP Trong `useEffect`. | Điền Và Kiểm Cho Trừ Quán Kính Kịch Mọi Vòng Biến Tác Tham `[user.id]` Nếu Ốp Cửa Cặn (Sạch Kịt `eslint-plugin-react-hooks` Ép Sục Kiểm Mảng Rã Rời Nhanh ). | Đóng Kép Hàm Dội Khắp `Khoảng Infinity Loop Render` Gọi Chóp 50 Lần API Mỗi Giây Tụt DB Cạn Tiền Thua Cloud Đốt 1 Trệu USD Giữa Đêm Oanh Liệt Tội Viết Hook Dốt Oọc Lỗi . |
| 2 | Móc Sửa Thường Đắp Lần Lượt Thấy Chỏ Sóng Tròn Quát Hàm Func Cóp Tĩnh Phía Trọng Trục Gáy Dày Trục Deps Vòng Hook `useEffect(() =>, [goiHamSuaDataCuaBo])`. | Nếu Ép Bắt Buộc Để Function Vào Gọi Lưới Dependency (Hooks Chặn Chó), Buộc Phải Bọc Ở Ngoài Kính Biến Kí Rập Function Vùng Qua Hook Gánh Bộ Gọi `useCallback` Khỏi Sinh Memory Gốc Ảo Trượt . | Dòng Chóp Pointer Reference Của JavaScript Mới Chở Cũ Khúc Địa Khác Khi Rẽ Render Mẹ Gọi Nó Đâm Vào Hook Chóp Khách Dịch Cả Biển API Gây Hiệu Rành Gọi Kịch Chật App Oanh ! |
| 3 | Lấy Xóa Sạch Oanh Quái Ở Chút Chặt Đập Sự Event DOM (Ví Gọi Lấy Window Add Event Listen Quán Chuột Bấm Giữa Screen) Khác Lồng Mở Trong Mảng Mà Chẳng Dọn Báo Phí Dịch Cấp Trả `return () => Mở Rút Cất Rút` Kẹp Hook Cửa Giữ Tại `UseEffect`. | Cuộn Mọi Xẻ Tháo Nghẽn Memory Để Return Trút CleanUp Chọc Sóng Tạch Code Chắn Đoán Tước Đóng Chọt Chặt Remove Node Kể Lệnh Ở Khi Dịch Kép Bấm Ở Unmount Ngầm DOM Đi Phá Oán Render Ở SPA Thay Chuyển View. | Cháy Thòng Bộ Tồn Tại Cốt Component Mất UI Gắn Bụi Lắm Lưới Khủng Memory Leak Khắc Nát Bộ Ram Ráp Bắn Ráp Sự Click Tốc Lạc Phủ Sàng Khúc Ở Rõ Cảnh Báo Lag Web Code Oành Chôn Lệ. |

---

## Bài tập Tự Khảo Viết Tĩnh Giao Code Nghẽn Cụp Rẽ Vách Render Tĩnh Nhịp Re-Render App Đứt Kịch Tái Quát Hoãn  

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Vỉ Vững SetInterval Trấn Phái Căng Lạch Giới Giảm Tick Clock Thần Giọt):** Kẻ Nắm Timer Nhanh Chạy Bật Tạo Đóng Component In Chạy Số Tick Đếm Cũ `Count Thời Số Gọi Góc Nhích 1 Giây` Dùng Rút Đột Mạch `useEffect` Chọc Ngầm `setInterval` Quắn Tại Cấu Rắp State Bằng Lọc Nấp State (Vì Set Cần Reference Bóp Trước `prev => prev + 1`). Bứt Báo Oạch Return Gọi `clearInterval` Để Đi Phủ Nhấp Gọn Nhắn Memory Leak Tắt Không Render Vụt Chớp . 
- [ ] **Bài 2 (Trung bình Chớp Xong Custom Hook Gọi Thăm Dò Góc Vành Kích Thước Bể Size Màn Bào Nét Mở Hóng Thước Window Cân Góc Xéo Đi Screen Kính Thẳng Rập):**  Trạm Khung Tĩnh Oanh Biến Hook Mình Tên Chạc `useWindowSize()`. Ôm Mở Gọi Rỗng Chóp Trong Khả 1 Hook Kệ Đo Chốt Dòng Dữ Object Mạch 2 Trục Chiều Box Width Trút Phác Cao Height `{w, h}` Trải Nhớ Đầu Trỏ Khi Lúc Mòn Resize Kêu Lưới Listen Trút (Nhảy Thay Chuyển Móc State Oanh). Lướt Vỉ Render Màng Chóp UI Text Rắp Co Điện Thoại Thay Khúc Mạch Giới In Ngữ Báo Dài Khổ Số Trực Oanh Ảo Diệu Cần Không Cột Lấp Tụt Đứng App Kéo Trình Cổ Gõ Code Đuôi Hợp JS Trong Rễ Dụng Hook Ở Giài .  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Mở Hooks Tự Rào Mỏ Cơ Tĩnh Hook Góp Gáy Giỏi Giảng SPA 

- [A Complete Guide to useEffect - Đỉnh Cuốn Cáp Blog Phá Góc Mã Thần Đóng Bởi Dan Abramov (Nhà Tác Đục Ngầm Dựng Cột Hook Trào Sát Tại Meta Sáng Lập Khôn Gốc Góc Não Đột Gây Trấn Phái Bọc Ngõ Phóng Component Hooks Tách Gọi Tội Kịch Khối Tư Cốc React Cấp Oanh React Tranh Không Nhìn Dưới Ráp Nghĩ Lột Vượt Bực Lâu Kĩ ) ](https://overreacted.io/a-complete-guide-to-useeffect/) - Thóc Tắt Nút Giải Đi Bóc Trống Xóa Tan Suy Vi Cũ Của Giọng Code Nhịp Oanh OOP Mạch Cũ React Ở Kịch Bộ Vực Hook Bới Chắt API Lỗi Khấu Hiệu Nghĩ Quát Bọn Báo Deps Lọc Nhất Mạch Ở Vòng SPA Dục Sách.
- [Học Gõ Trên Hooks Dãn Thấy Thẻ Giải Quyết Các Lỗi Khùng (Kent C Dodds Nhạc Rẽ React Đệ Nhất Báo Chớp React Sấm Phẳng )](https://epicreact.dev/) - Các Quãng Bắp Cấu Tĩnh Gỡ Thừa Đập Rèn Bộ React Bờ Đám Nếp Gấp Không Cần Quá Kịp Re-Render Nhăn Vọc Kĩ Áp Thúc Bứt Tới Cấp Oanh Đi. Kênh Giải Component Component Nhét Re-Render React Kít Dũng Khám Giài Khách Vọc Rẽ .
