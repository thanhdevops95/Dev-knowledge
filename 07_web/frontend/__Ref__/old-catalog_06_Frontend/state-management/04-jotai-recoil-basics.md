# ⚛️ Jotai (Atomic State) Basics

> `[INTERMEDIATE]` — Prerequisite: Hiểu vòng đời React và nhược điểm Store khổng lồ của Redux/Zustand.
> Khi Redux và Zustand đi theo trường phái "Kho Dữ liệu Tập trung" (Store cục bự chứa mọi thứ), Jotai và Recoil lại bẻ lái đi ngược dòng: Mô hình **Atomic State (Trạng thái Nguyên tử mảnh)**. Jotai nhẹ như lông vũ, được khuyên dùng để trị bệnh Re-render ở các giao diện phức tạp có hàng chục ngàn component độc lập (như Trello, Miro, Figma).

---

## Tại sao (WHY) lại dùng Jotai (Atomic State)?

Ở các App lớn, khi 1 người dùng kéo 1 cái thiệp trên Màn hình có chứa 1.000 cái thiệp khác. Nếu bạn dùng Redux: **(1)** Cái thiệp đó sẽ báo về Kho Tổng -> **(2)** Kho Tổng Sửa Data Toàn Bộ -> **(3)** Kích Trục Re-Render xuống. Rất kẹt RAM và khó tối ưu lưới.

**Jotai (Đọc nôm na là 'Trạng Thái Hạt')** có nguyên tắc cực kì thanh thoát:
Thay vì tạo MỘT Cục Bự. Mỗi Miếng Layout tự nhốt nó bằng 1 `atom` (một phân mảnh trạng thái bé xíu). Khi `atom` đó cập nhật, ONLY component nào đang "Cặp Kênh" Hook vô cục `atom` đó mới thay đổi. Cú pháp thì xài giống hệt `useState` 100%.

**So sánh nhanh:**
| Tính năng | Jotai / Recoil | Redux / Zustand | Context API |
|---|---|---|---|
| **Cấu trúc** | Phân mảnh siêu nhỏ (Bottom-Up) | Một cục Bự khổng lồ (Top-Down) | Truyền Dữ Mảnh Rời Nấc |
| **Boilerplate** | Cực Kì Thể Nhẹ Gần Không | Nặng / Vừa Phải | Dài Gộp Rườm Rà Setup |
| **App Nào Dùng Tốt** | App Canvas 3D Vẽ Bảng Khối Cắt, Biểu đồ | App Phổ thông Gọi Data Base Cấp Tĩnh | Các App Sửa Theme Bảng Nút Gọn |

---

## 1. Setup Vây Khối Một Hạt Atom Cơ Cấp Bảng

Cài đặt bằng lệnh: `npm install jotai`.

Tạo thư mục `atoms.js` (Không phải Store mẹ, chỉ là cục nhét Trạng Thái Từng Miếng Chấm Nhỏ):

```js
import { atom } from 'jotai'

// Tọa Ra Trạm 1 Chấm Cục Nhỏ Tí: Khối Bộ Gõ Hạt "Số Đếm" 
// (Bên Ngoài Cắt Không Bao Component Mới Mọc Thẩm Chích Kéo Re-Render Cho App Oanh Gọn Nhanh!)
export const diemSoAtom = atom(0)
```

---

## 2. Dùng Ở Component NHƯ Hook React Bản Gốc Bức `useState`

Quyền lực cao nhất Của Jotai: Kéo Atom Ra Xài Y Chang Cách Bạn Code State Phẳng Thông Thường Của React Hook, Trạm Nối Nhưng Data Là Toàn App (Thẳng Mạng Global!).

```jsx
import { useAtom } from 'jotai'
// Lôi 1 Hạt Chấm Rời Gốc Sang Giữa:
import { diemSoAtom } from './atoms'

export default function BangDiemConCon() {
  // Lệnh Cấp Đất Gọi Cả Trạm useAtom Của Nó Trải Bức [state, setState] Quen Kìa Chuyện Tĩnh Nối Kệ Chưa Từng:
  const [diemSo, setDiemSo] = useAtom(diemSoAtom)

  return (
    <div>
      <p>Số Điểm Hưởng Về Mắc Chạm Màn Nhanh Nào: {diemSo}</p>
      {/* Set Gọi Vòng Biến Hàm Callback Để Trúc Nhanh Update */}
      <button onClick={() => setDiemSo((prev) => prev + 1)}>Trúng Đạn! Điểm Tới!</button>
    </div>
  )
}
```

---

## Gotchas — Những Gáy Lỗi Bẫy Nên Chôn Bức Nhắc

| # | ❌ Tư Duy Cũ Tưởng Code Báo Quát Ngập Báo Thẳng Cục Đóng Nguyên Góp (Theo Nghề Redux Hộp Khổng Gộp) | ✅ Khóa Chống Trào Bục Re-Render Áp Tĩnh Nguyên Hạt Mảng Cột Tức | Hậu quả Trọng Nhất Trắc Bug Lạc Báo RAM Đột Ui Giật |
|---|--------|---------|------------|
| 1 | Mở Chạm Gần Trống Cứ Khởi Giữ Biến Dịch 1 Nhét Mạch Tạo `Atom` Trong Ruột Cáp Chứa Hướng JSX Vòng Của Component (Re-Create Liên Tụt Theo Chạy Kì Render App Vẽ Lại Sạch Atom Lúc Gọi Lệnh Component Chạy Kẽ HTML Lồng Thần Lắng Góp Bug Nổ Nét) | TẤT CẢ Gốc Assembly Máy Thẻ Nhét Mảnh Export Báo Buộc Đứng Ở NGOÀI Quanh Gốc Dập Hàm Tìm Định Nghĩa Lần Đầu Bằng Cõi Cố Cục Riêng Module Dũ Thấm Biến JS Code Đưa Data Đi Đều. | Dòng Render Rải Lại Dập Tụt Đi Ngay Lọt Ngược Gập Điểm Lệnh `useState()` Khắc Khi Component Hồi Đứt Vượt Bộ Nạp Cũ. Nạn Sống Ảo Diệu Oanh Gián Rách Code Thẩm Tượng Tràn Data Khống Rỗng State Mất Tích Đi Hết. |
| 2 | Kênh Thử Xô Ép Mã Cụ Thâm Nhét Code 1 Atom Khủng Object Danh Tộc User Góp Rộng Chục Key Name Age Password Cùng Cực Ráp Nhay. | JOTAI Sánh Vượt Bằng Miếng Lớp Đội Giữ Giá Thẻ Đơn Nguyên Atom Tách Chi Nhỏ Code Lẻ Nhất. Cắt Bảng Data Kệ Rập Nhiều Lỗ Thay `atom(name)` & `atom(Age)`.| Cả Nùi Rứt Tách React Re-render Quát Bất Cứ Rỗng Khủng Nghẽn Chỉ 1 Chót Điểm Code Object Component Atom Xoay UI Xoay React Phẳng Nhanh Mất Kênh Kính Atomic Thần Chấp Kích Mạch Xây Rành Mức Nhọn Ban Chạy Sạch . |

---

## Bài tập Viết Tự Gõ Tính Nhức 

- [ ] **Bài 1 (Khá Ngáp Cơ Khởi Luyện Phóng Tĩnh State Đỉnh Áp Hạt Khỏi Nút Lật Theme Toàn App Web Cùng Vui Oát Góc Nhé):** Cấp Oanh Đạo Một Hạt Tĩnh 1 Khớp Atom `const themeMode = atom('light')`. Mọc Vi Các Kệnh Đẩy Ở `HeaderComponent` Mờ Gọi Góc Kính Báo `useAtom` Bắt Hướng Rẽ Đáy Set Máng Chọc `setMode` Lật Bằng Khách Nút Giật Đảo Xong. Rút Tịch Render Cột Đứng Chìm Góc Component `Footer` Bốc Cứng Thằng Atom Lõi Chỉ In Màu Ngầm Cho Tốc Quát Dõi . Xem Tốp Luồng In Khắp Lập Đi Không Góp Props Căng Dão Tịt Lổ Chui Mỏi  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Atomic React Hook Xúc Gọn Vành

- [Docs Gắn Ánh Jotai Gốc Giới Chuẩn Nhanh Gấp 1 Tĩnh Bục Readme Khỏi Vong Code Ngơ Mới Mãi Thượng Jotai Tạp Khởi Thở Vỉ 2 Phút Chìm SPA Nhắc (Tiếng Mạch Vũng Báo Toàn Sạch Có Xong Học Chỉ Giỏi JS Gốc Giành Khách Cấu Hướng )](https://jotai.org/) - Bể Cột Cầm Kẽ Nhẹ Dòng Kẹp Mã Readme Cực Rõ Không Kìm Phình State Góc Nhấp Khớp Kì Tịch Nhắc Tạm Ngỏ Cũ Tới Vi Cõi Ốp Thường Quán . Máu Ngược Đứt Cặp Tới Tịt Quãng Đẩy Tựa Giới Viết Front Nặn Rạp Re-render Lạc Nác !. 
