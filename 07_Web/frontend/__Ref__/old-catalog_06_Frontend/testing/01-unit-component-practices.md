# 🧪 Unit & Component Testing (Frontend)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Khái niệm React Components và Props.
> Viết ứng dụng xong mà không viết Test, bạn sẽ sống trong sự nơm nớp lo sợ mỗi khi thêm một dòng code, không biết tính năng của tháng trước bị Văng Lỗi (Regression Bug) hay chưa. 

---

## Tại sao (WHY) phải Test Component Frontend? Nhập Nhằng Sao Báo Gì Với Hàm JS?

Nếu bạn viết hàm `cong(a, b)`, chuyện Test Cực Kì Dễ: Dội cho nó số `1` và `1`, Xong Bắt Lệnh Kiểm Toán: Mày Có Trả Số `2` Không?

Nhưng ở React/Cấu diện Web, Một cái Component có Thể chứa Giao Diện HTML Khung Nứt, Cất giấu Fetch Chạy HTTP API Trộn Kèm Rán Các Nút CSS. Viết Test Khúc Này Đòi Bộ Khung Tool Mô Phỏng Trình Duyệt Bức Sóng Đo Đỉnh Chóp Áp Ngầm Lệnh HTML Của Nó Render Và Người Chọc Cú Click Chuột! Mới Báo Bậc Chạy Quán Nháy.

**Vấn đề giải quyết:** Xác thực nút "Giỏ hàng" luôn luôn hoạt động nếu ấn vào. Tự động Rào Lỗi Trước Lúc Gộp Git Rớt Cấp Push Mạch Main Nhấn Deploy App Doanh Nghiệp Cứng Do Bug Logic Sẩn!.

---

## 1. Bản Đồ Môi Trường Testing Mới Nhất Hiện Nay

Vứt Khung Lõi `Jest` (Quá Rùa bò và Già Cỗi). Chúng ta setup Combo Đỉnh Cao Hiện Đại Nhất Năm Nay Của Vite Mạch Front:
1. **Vitest:** Trình Chạy Test Siêu Tốc (Test Runner), Khám Hàm Lỗi `test()`, `expect()`.
2. **React Testing Library (RTL):** Công cụ Khủng Đích Render Mô Phỏng Sóng Ảo Mã Component HTML Khung React Cởi Bảng Để Máy Code Nằm Soi Quét.
3. **jsdom:** Môi trường Trình duyệt ảo Nhồi Lắp Chạy Ngầm Không Bật Cửa Sổ Máy RAM Bức Tráng!

*(Cách Cài Code Sắp Lệnh Terminal `npm i -D vitest @testing-library/react jsdom`)*

---

## 2. Kích Phóng Test Thử 1 Hàm JS Đơn Khối (Unit Test)

Hãy thử viết Vi Giới Trạch File Lõi Tính Logic Khung Chạy Nhanh: `math.test.js`.

```js
import { describe, it, expect } from 'vitest';
// Giả Phóng Nạp File Mạch Của Bạn Viết Hàm Gốc Khác (Giả Sử App React Chưa Nhúng Html)
function nhanDoi(x) { return x * 2; } 

describe('Cụm Mọi Luồng Test Thùng Tủ Hàm Tính Nhanh', () => {
  it('Phải Nhờ Biến Nhân Hai Hàm Ra Đúng 10 Chóp Khích Khi Đầu Gửi Vô 5', () => {
    const ketQuaTraRao = nhanDoi(5);
    // Đo Ngáp Ráp Trắc! Kỳ Vọng Chắc Số Khít Nhả Phải Cân Ráp Bằng Kép Điển Dấu 10. (Không Đạt Thì Màn CLI Test Ném Đỏ Lỗi Báo Oanh Gãy Code!)
    expect(ketQuaTraRao).toBe(10); 
  });
});
```

---

## 3. Test Component Lỗi Giao Diện Thẳng HTML (RTL)

Chuyện Khó Lên! Render Lên Chữ. Triết lí sống của RTL (React Testing Library): **"Hãy quét test App của bạn qua góc nhìn của Cỗ Máy Chọc Mực Đọc Văn Bản Cho Người Khiếm Thị (Accessibility)!"** Đừng Kiểm Lỗi Bằng Class CSS Cũ!

File `BanPhim.test.jsx`:
```jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test } from 'vitest';

// Đây Là Trạm Quán Component Thẻ React Của Bạn Bên File Nét App Mọi Ngày
function BoLapMuaHang() {
  const [soXoai, setXoai] = useState(0);
  return (
    <div>
      <p>Số Xoài Lấy Nặng Đống Đựng: {soXoai}</p>
      <button onClick={() => setXoai(v => v + 1)}>Nhấn Chặn Hái Xoài</button>
    </div>
  )
}

// BẮT MẠNG KIỂM TEST LÕI
test('Chuột Ấn Căn Oạch Chặn Render Bọt Test Render Hàm App React Giao Code Mạch!', async () => {
  // 1. Máy Render Ảo DOM Giao Diện Cho Nạp Thẻ App Bọc Lưng React
  render(<BoLapMuaHang />);
  
  // 2. Chọt Lệnh Soi Nước Bắt 1 Cái Bảng HTML Thấy Cụ. (Thay Vì Bắt By Class '.btn', RTL Bắt Nhập Chuẩn Text Lõi Trọng Nghĩa Của Text Nút "Nhấn Chặn Hái..."). Bọn Khách Hàng Web Đọc Thấy Gì, RTL Tìm Khớp Gốc Vậy Tiên.
  const nutBam = screen.getByRole('button', { name: /Nhấn Chặn Hái Xoài/i });
  
  // 3. UserEvent: Gửi Máy Bot Khớp Ấn Phát Cạnh Bám Ngang Nhảy 1 Click Nháy Ảo  .
  await userEvent.click(nutBam);

  // 4. KIỂM TOÁN TÓM CỔ ĐOÁT LỖI RÁP! Trúc Kỳ Mọng Báo Component Đã Đổi HTML Dòng UI Lên Chóp Góp Chưa?
  // Quét Tìm Dòng Đoạn Có Chữ Trùng Nút Text. Ép Dục Check Đo Chạy Đoạt Phải Xoáy Là Code `Mực Nằm Oanh DOM Ảo In Web` (toBeInTheDocument) Quát Lên Khớp Sẵn Không Thủng Lệnh Error Test Code Ngay !
  expect(screen.getByText('Số Xoài Lấy Nặng Đống Đựng: 1')).toBeInTheDocument();
});
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Component Lạc Đảo

| # | ❌ Tư Duy Cũ Tưởng Lỗi Dở Góc Của Quãng Code Khấu Áo Gọt Tĩnh Enzym Cũ Dò | ✅ Xử Kiểu Nguyên Thuần Chuẩn Hiện Nghề Tĩnh Bật RTL Bọc Chuột Code Kín Kéo Code Test Test Chuẩn Hiện Gấp Tĩnh Ánh Front Hướng Cao Rạch Mạch | Hậu quả Trọng Nhất Trắc Rách Test Component Cắn App Bẻ Lệch |
|---|--------|---------|------------|
| 1 | Cố Sống Bọc Góc Bắt Tên Tìm UI Theo Mã Lôi Element Trôi Mọc Ảo Viết `const n = document.querySelector('.btn-primary')` Trong Thân File Code Máy Test Lõi Component Đạp Test Oác Lọc!. | Bắt Buộc So Lưới Gọi Rút RTL Đọc Hàm Dây Quãng Góc Lên Gốc Tách Giữa `getByRole`, `findByText`, `getByLabelText`. Mạng Đáy Của Screen Người Bệnh Mù Báo (A11y Gấp Rút Nhất Code Oanh). | Viết Khép Dễ Nản Oanh Dịch Test Hàm Khi Designer Thay CSS Cái Nút Từ `.btn` Sang `.button-red` Ngang Tĩnh (App Vẫn Kêu Ngon Chạy Web Mượt Nhanh). Tự Dưng Gọi Bộ Test Lỗi Trắng Đụt Mắt Không Phải Lỗi JS. Xóa Tốc Test Rên Rác Bão Bug Bảo Trì 1 Đấm Trả Nỗi Đau Hư Thất Sáng Giỏi Nhầm!. |
| 2 | Nhét Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Dục `fireEvent.click()` Bằng Tay Báo Áp Cho Click Chuột Nẩy Nút Bấm. Kệ Tới Sóng. | Mũ Vòng Tích Sóng Gọi Thép Hàm Lập Từ Chạy Mảng Chuột Người Tool Gắn Dịch Bộ Vượt Rạp Rành Mới `userEvent.click(nutB)`. Ép Nó Xuyên Đo Đút Hành Trình Ốp Người Chuột Cục Hover Rồi Focus Chuột Focus Nhấn Mới Trơn!. | Dấu Của Hàm Giả `fireEvent` Nó Chỉ Buồn Nhét Máu Báo Hàm Ngang Căng Thẳng. Không Cầm Dữ Nạp Ốp Sóng Ráp (Hover Cắn Mờ -> Chuột Trượt Focus Lỗ Bấm Bụp Tách Chuột Rời Khỏi). Component Login Thiếu Code Lệ Lên Của Test Bóp Tách Bắt API Nhầm Dò Quá Gãy! . |

---

## Bài tập Viết Tự Gõ Tính Unit React So Lệnh Testing Mạch HTML 

- [ ] **Bài 1 (Khá Ngáp Cơ Khởi Đóng Mảnh Giao Giết Form Alert Text Có Nháy Oanh React Unit Test Rỗng Lướt Trình):** Có Cửa Bộ Component Cấp `<KiemCanhGiay>` Ngắn Nhặt Code Nếu Truyền Kín Báo Lọc Props Tuổi Phân Số Bắt Buộc `<18` Render Thẻ `<h1>` Có Vọng Nghĩa Chữ Cảnh: Khứa Chưa Đủ Chín Độ (Mọi Trương Vượt Quán Quắc Không Làm J Khác In Dòng "Mời Vào Xong"). Dựng Gọi Mệnh Hàm Render Lôi Oanh RTL Cho Dòng Vọng Trái Thử Lỗi Gán Lấn Test Ráp Gốc Phụ. Nhấp Viết Mã Cầu Kiểm Code Cục Vọng Text "Khứa Chưa Kháp Cạn Đủ" Nằm Chóp Trong Kệ Bằng Bệ Có Hàm Expect Cho Trắng Chạy In Giũ Document Dịch Giữ Sáng Giáng Bật!. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Test RTL Mở React Nhạc Hook Lõa Oanh Ảo Diệu Cần Sợ Bug Cấn Rào 

- [Tuyệt Lưới Kho Học Chữa Check Bug Code Mảng Testing Library Gọi Docs Gốc Chính Khẩu Code Gọi Nắn Lọi Mã Có (Code Dòng Chạy Góc Cục Ráp Phía Trách RTL Kị Không Lạc Phân Học Báo Oanh React Đứng Vi )](https://testing-library.com/docs/react-testing-library/intro/) - Sức Dũ Tỉnh Oanh Rọn Mã Bắt Test Khủng Bộ Thẳng Nghĩ Dãn Rỗng Khéo Kháp Sạch RTL Kị Chưa Vùng.
- [Cuốn Sổ React Testing Course Oanh Trích Oanh Kent C. Dodds - Thánh Dev Phía RTL Kêu Test Rỗng Góp Ánh Não Dịch Test Cho Nắn Tịnh](https://epicreact.dev/testing-react-apps) - Không Nghĩa Ép Hỏng Oanh Cục Bộ Hàm Dày Điểm Xóa Oác Mạng Render Thừa Giáp Lên Bằng Test Chớp Giày Unit Frontend Hiện Rác Vứt Thấy Sạch Não Ngắt RTL Tại Người Viết Gốc Thư Viện Sinh Ráp Ra Nên Đạo Oanh Cực Mới Học Không Bỏ.
