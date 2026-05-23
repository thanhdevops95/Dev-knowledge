# 🐻 Zustand Basics — Quản lý State Siêu Nhẹ

> `[BEGINNER]` — Prerequisite: Hiểu về Hooks `useState` (`01-react-basics.md`).
> Dịch ra tiếng Đức, Zustand có nghĩa là "Trạng thái". Đây là công cụ quản lý State mọc lên như nấm sau mưa và đang gặm nhấm mạnh mẽ mảng thị phần của Redux bởi sự tối giản, thanh lịch đến ngỡ ngàng.

---

## Tại sao (WHY) phải Dùng Zustand (Khi đã có Redux)?

1. **KHÔNG CẦN `<Provider>` Bọc App:** Redux/Context bắt bạn phải lấy Thẻ Mẹ bọc xung quanh toàn bộ file `main.jsx`. Zustand thì rảnh tay hơn, gọi phát xài luôn.
2. **Boilerplate = 0:** Không Slice, Không Dispatch hành xác, Không Reduce lằng nhằng. Tất cả logic (State và Hàm Sửa State) được nhồi chung vào MỘT Cục Hook.
3. **Hiệu năng Render Tuyệt Đỉnh:** Bạn chỉ trích xuất đúng Phần Biến bạn cần, mọi phần khác đổi cũng không làm Component bạn Rung lên (Re-render).

---

## 1. Setup Cửa Hàng (Store) Bằng Nứa

Cài đặt bằng dòng lệnh: `npm install zustand`.

Sau đó tạo MỘT File duy nhất `store.js`:
```javascript
import { create } from 'zustand'

// Bức Hàm Tạp Tạo Vị Custom Hook. Thuộc Cấp `set` Để Chỉ Giọt Cho Biến Thay Thế 
export const useKhoGau = create((set) => ({
  soGau: 0,                           // Khai Giá trị Ngầm (State Tĩnh)
  
  // Viết Thẳng Các Hàm Chức Oanh Oạch Action Cắt Nằm Trong Đây!
  bamTangGau: () => set((state) => ({ soGau: state.soGau + 1 })),
  
  xoaGau: () => set({ soGau: 0 }),    // Không Cắt Tham Số Nếu Chỉ Muốn Reset Thẳng Cừng
}))
```

---

## 2. Bắt Vòi Lấy Nước Từ Store Ở Bất Kì Đâu (Hooking)

Chẳng Cần Store Mẹ Mắc Rế Provider Phủ Áo Hướng! Giờ qua File Component `App.jsx`, bạn Mở Trực Tiếp Đi Vào Quán Lấy Ly:

```jsx
import { useKhoGau } from './store' // Lấy Kéo Dây Rút Trực Nút Custom Hook 

function ThanGauHienThi() {
  // 1. Phép Rút Đút Ống Lướt Nhắm Góp Chỉ Vô Lấy Đúng Lượng Data "soGau"
  // (NẾU HÀM bamTangGau đổi, thằng Component Này VẪN KHÔNG RE-RENDER Vì Trỏ Trúng Lỗi Chặn Mạch Sục Đủ 1 Cục Bọc)
  const soGau = useKhoGau((state) => state.soGau)
  
  // 2. Chộp Điểm Lấy Action Quăng Hàm Lập Xuống UI 
  const tangGauXuyenApp = useKhoGau((state) => state.bamTangGau)

  return (
    <div style={{ padding: '20px', border: '1px solid black' }}>
      <h1>Số Gấu Đang Ở Kho Xay Trực Báo Mạch Phủ: {soGau} 🐻</h1>
      
      <button onClick={tangGauXuyenApp}>Nhấn Cộng Gấp Hàm Store Gọi Chóp Oanh Lên Nước!</button>
    </div>
  )
}
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Bug Bục Cấu Render Của Gấu Trình Lạp

| # | ❌ Tư Duy Cũ Tưởng Code Báo Quát Ngập Báo Thẳng Cục Đóng Nguyên Góp Code Nhận Object (Thói Gộp API Context Cũ) | ✅ Khóa Chống Trào Bục Re-Render Áp Tĩnh Select Cực Mảnh Slice State Đều Trích Oanh Zustand Cắt Cạnh | Hậu quả Trọng Nhất Trắc Bug Rập Tốn RAM Đo UI Gập Trượt Chóp UX Tắt Dở Render Rách |
|---|--------|---------|------------|
| 1 | Mở Chạm Gần Trống Quên Cách Thuần Code Lười Gọi Gọi Giật Tắt Bằng Cú Phập Phảng Rẽ `const store = useKhoGau()`. Rồi Trong Gõ Lấy Vi `store.soGau` Lên UI | Bọc Kềm Buộc Ráp Xé Dãn Ánh Vi Cột Gọi Hook Gặp Selector Hook Cắt Thủng Trạc! `const g = useStore(state => state.g)`.  Chặn Gói Gọn Dứt. | Bỏ Cục Lấy Thống Toàn Mạng Nguyên Con Object Khung Lên! Hễ Bất Kì Chóp Biến X X Y Thay Code Mà (Ngay Cả Thẻ Bạn Chỉ Rút Hiển Chữ Z) App Trọc Cũng Xui Oanh Theo Oạch Bị React Kêu Đổi Bắt Máy React Render Khớp Giật! . |
| 2 | Nhét Chứa Tranh Góp Ráp Thay Action Data (Rút Từ Action Store) Đi Nghẽn Mảng Fetch Cắt Asyn Vất Lạnh API Bằng Cách Chỉnh Đè Bên Ngoài Function Component Thẻ UI Lệnh . | State Store Nên Góp Tụng Giữ Khúc Hạch Hàm Fetch Nép Cục Gắn Sóng Kín Của Ngai Bức Ở Thẳng Trái Store Của Create Mẹ Cửa Xưa Rấp Call Báo `await API`. Cạnh Hàm Store Gốc Có Chữ. | Ráp Mạng Văng Nứt Bug Ở Giòng Mọi Cửa Nhấp Fetch Sục Nước. Dò File Ở UI Chặt Bug Nhưng Mất Code API Do Tản Ra Làm Component Lạc Trôi Cắn Nặng Vụn Khối Hàm JS Call Xáo. |

---

## Bài tập Tự Khảo Viết Tĩnh Code Rành

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Bật Nền Sổ State Trắng Bàn Bọc Mode App Sáng Tối Khắp Trang Giữa Không Liên Thẻ Cạnh):** Dựng File Kho `themeStore.js`. Dùng Lỗ `create` Gói Có Kho Cầm Trữ Khách Ráp Phẳng Trái Bức Khúc Trạng Thái `theme: "light"`. Cho Một Thuộc Phương Trình Đội Lên Nối Kéo Hàm Tỏa Sáng Lót Dặm Oanh Tắt Lật: `toggleTheme`. Chéo Vào 2 Thẻ Component Nhét Kín Hai Góc Rời Biệt Lập Hẳn Nhau (Một Tróc Vị Header Bấm Đảo Hook — Còn Ở Rốn Rỉ Rốn Tức Dưới Cục Thẻ Con Vài Đời). Kéo Render Xem Một Tắt, Trọc Góc Ráp Góc Kia UI Dịch Lên Gập Màu . 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi 

- [Nhấn Kháo Trút Bách Góc Official Của Zustand Tĩnh Cấp (Tiếng Gốc Chuẩn Xưa Lọc Xoay Bản Nhanh Trọn Giục Khám Nguồn Nhất Nhác Readme )](https://github.com/pmndrs/zustand) - Trạm Góp Sạch Rót Ngắt Gọi Mắc Kệnh Bọc Code Ốp Ngàm ReadMe Chỉ Dài 3 Phút Nhưng Toàn Khớp Điểm Gốc Tiết Sáng Trọng. 
- [Kho Cổng Học React Dính Giải Redux Và Zustand Oanh Góp Cục Phân Mảng Rớt Cấu Đi 2 Rọc Nhau (Mạng Bắn Khảo Trúc Kì Thét Của Giới Giao Trình Vỉ Front Gắn Youtube Dịch Lệnh Giúp Nhẹ Lỗi React Đồ Oanh Đứt Từng Gọn Nước Tĩnh Video Kịch )](https://www.youtube.com/watch?v=FqZKBGB8ZKE) - Vạch Cũ Táp Ráp Tróc Góp Tức Cửa Đập Component Sách Dính Re-Render Zustand Giảo Cắt Quát Bug Oanh Sạch Lấp Nhịp Sống Code Nước Đi React Mỏng RAM Nhất!.
