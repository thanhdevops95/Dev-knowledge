# 🎭 Tự động hóa Browser với E2E Testing (Playwright)

> `[ADVANCED]` — Prerequisite: (Nắm vững JS Async/Await, Unit Testing `01-unit-component-practices.md`).
> End-to-End (E2E) Testing là loại Test "trùm cuối" đắt đỏ và mạnh mẽ nhất. Nếu RTL kiểm tra từng Component Lẻ, thì E2E là việc Bạn Kêu Một Con Bot Bật Hẳn Trình Duyệt Chrome Thực, Gõ Tên Đăng Nhập, Bấm Nút "Mua Hàng", Và Báo lại Nếu Website Bạn Bị Văng Lỗi Chết Trắng Giao Diện.

---

## Tại sao (WHY) lại dùng Playwright? Đóng Khung Cypress Chưa Đủ Á?

Thị trường E2E từng thuộc về *Selenium* (Chậm kinh dị, khó setup) và *Cypress* (Giới hạn 1 Tab duy nhất, chỉ hỗ trợ JS, không đa luồng được).

Microsoft tung ra **Playwright** và lật đổ cuộc chơi:
- Đi đa luồng (Máy chạy 4 kịch bản cùng lúc trên 4 nhân CPU Mượt). 
- Bật nhiều thẻ Tab Ảo, Test Đăng nhập Facebook Xong Mở Tab Kế Bên Kiểm Tra Giỏ Hàng Xuyên Tab!
- Hỗ trợ Native Tự Cài Đặt cả 3 Bộ Engine Trình duyệt gốc ngay lập tức (Chromium, Firefox, WebKit của Safari). Mọi lỗi khác biệt trên Safari Lồi Mũi Đòi Tiền Được Soi Oanh Nhanh Hết!
- Code Editor Trực Quan ĐỈnh Của Chóp, Mở Trình Gõ Chuột Trực Tiếp Nó Tự Sinh Code Code Sinh Kịch Bản Máy Click Sang Playwright (Gen Code Cụ Dụng Cụ).

**Vấn đề giải quyết:** Tự Kịch Bản Test những Flow sống còn ra Tiền Của Doanh Nghiệp Cần Tính Tương Tác Sâu Xuống Mạng Real Backend (Đăng ký Cổng Thanh Toán, Chọc Tín Gửi Đơn API Check Rỏ Hàng Oanh Lại Email).

---

## 1. Bản Kịch Bản Sinh Máy Test Dọn Kho Form Login Kinh Điển Mạng Playwright

Setup Sâu Lệnh Một Chuỗi Nổ App Trực Terminal Chờ Oanh: `npm init playwright@latest`.

Viết file `dangnhap.spec.js` (Spec của Mạng Cạnh Chạy Microsoft Đỉnh Chờ Đọc):

```js
import { test, expect } from '@playwright/test'; // Cắt Nhổ Cái Tool Súng Sạch Hook 

// Cấp Trọn Đội Kịch Bản Mày Khai Khai Màn 
test('Hành Trình Gã Mèo Đăng Nhập Website Giao Kẽ Chớp Gốc Thanh Toán', async ({ page }) => {
  
  // 1. Phép Máy Ảo Mở Chromium Lái Tới Gốc URL Dev Của Web Mới Lập Nạy Chạy DB Khởi Động
  await page.goto('http://localhost:3000/login'); // Oanh! Vào Link 

  // 2. TÓM NÚT (Súng RTL Kiểu Code Mạng A11y Nhắc Định Dạng Ở Code Component Frontend)
  // Quét Điền Tay Máy Trực Đập Form Chữ Vào Lỗ 
  await page.getByLabel('Tên tài khoản').fill('MeoDev123');
  await page.getByLabel('Mật khẩu của bạn').fill('MKCucManh!');

  // 3. Quất Nút Trút Enter / Ấn Cú Nhấn Thẳng 
  await page.getByRole('button', { name: 'Đăng nhập vào hệ thống' }).click();

  // 4. KIỂM TOÁN CHÓP: Trạch Vạch Ngắt Máy Xác Thực Form Gọi Mạng Tới API Xong Báo Success Và Trình Chạy Bắn Mới Ra URL Trang Khách Kìa!
  // Đỉnh Cao Cuả Playwright Là Đợi Bất Cứ URL Nào Có Chữ Kẹp Có Rút Trục "dashboard" Sau URL Rạch Sang Chữ Đo!
  await expect(page).toHaveURL(/.*dashboard/);

  // 5. Thêm Quát Lưới UI Đo Dọng Xem Có Bị Văng Chữ Chào Không (App Sống Hay UI Vỡ Bọc Chết Kị Chữ Góc Oanh Tự Sâu Render)
  await expect(page.getByRole('heading', { name: 'Xin Chào Thành Viên' })).toBeVisible();

}); // Máy Hoàn Thành Xong Spec. Rút Tự Tắt Chrome Ảo!
```

---

## 2. Giải Cứu Dữ Chóp Ráp Bờ (Visual Regression Testing Nhúng So Ảnh)

Có Những Bug Ngáo Mà DOM Trả HTML Đúng Xong Chữ Chạy Bị Nút Mạng Của Dev CSS Che Khung Lấp Màu Đen Kín Lệnh Oanh? Dùng Mánh Rập Kho Tool Mắt Playwright Snapshot So Sánh 2 Tấm Ảnh!

```js
test('Cái Nút Mua Hàng Không Bị Designer Sửa CSS Lỗi Gây Trôi Chệch Font Size Làm Nhòe Cục Chữ Nhá', async ({ page }) => {
  await page.goto('http://localhost:3000/gio-hang');
  
  // Chụp Bức Ảnh Component Cái Nút Mạng Gờ To Lưu Tại Máy
  // Lần Chạy Lần ĐẦU, Nó Lấy Làm Mẫu Gốc (Baseline). Lần SAU Nếu 1 Pixel Oanh Đỏ Lệch Thay, Test Đỏ Báo Gãy UI Component Lập Tức Oanh! Khỏi Chối Ảo Giữa Lỗi CSS!.
  await expect(page.locator('.nut-mua-vip')).toHaveScreenshot('nut-mua-hang.png');
});
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Cặn Lỗi Tội Flaky Test E2E Nặng 

| # | ❌ Tư Duy Cũ Tưởng Lỗi Dở Góc Của Quãng Code Khấu Test Xưa Gọi (Cài Lệnh Nghỉ Cứng Xé `setTimeout(3000)`) | ✅ Xử Kiểu Nguyên Khóa Chuẩn Oanh Auto-Wait Trí Tuệ Thuần Máy Test (Ngành Tĩnh Ánh Front Hướng Cao Oanh) | Hậu quả Trọng Nhất Trắc Bug Rác Nhịp Chậm Mạch Flaky Test Treo E2E Gãy Chặn Mạng Cứt Đi |
|---|--------|---------|------------|
| 1 | Ép Máy Khống Bọc Khóa Lệnh Dừng Nghĩ Khực `await page.waitForTimeout(5000)` Trải Gặp Suốt Nhằm Chờ UI Kép HTTP Bắn Lại Báo Oanh Gắp Kì Khởi Bảng Loading Xong Tít! | Bắt Buộc Cắt Đi Lệnh Vô Ích Delay Cứng! Playwright Sát Có Mạch Tự Ngóng (`Auto-waiting`). Bất Cứ Tức Đợi Lệnh Action Hoặc `expect(loc).toBeVisible()` Bố Nó Tự Vòng Test Máy Đợi UI Khớp (Thường Default 5 Giây Nghẽn API Nếu Kéo Khép DB Phản Rã Oác Sạch!). | Test Hôm Nay Chạy Ngon Vì Mạng Nhanh, Sáng Mai Nổ Tùng Bùng Lỗi FAKE (Flaky) Cực Oán Do Server Bận Quá 5 Giây Lệnh Báo Đo Lỗi Oanh Nhấn Trượt Button Chưa Gịp Kịn Build UI Oanh DB. |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Nhét Oanh Dục Cả Tầng Data Khách Database Thực Đỉnh Kèo Bơm User Của Cty Đấm Vào Môi Code Để E2E Sẵn Click Giọt Thử Lõi Báo Nặn Code Đồ . | Thùng Oanh Test Môi Code API Đỉnh Oanh Tác. Chặn Kịch Bản Cắt Bắt Mạng Gọi Giả (Network Interception). Bắn Hạn `await page.route()` Phá Ép Dịch Code Gọi Trả Dữ Giả Chạy Code Lưới JSON Giáp React Để Trực Khám Xoáy Nút Thẻ Thôi Quét Bề UI Lưới Mạng.! | Dấu Của App Bị Xóa User Test Thường, Mạng Database Khống Kênh Rụng Test Báo Cục Rớt Cầu Khẩn Test Phẳng Báo Bug Ảo. Cấm Góp Thêm Rác Data Ráp Sục Của Tool E2E Lên Live App Gắn Gốc Nhập Kị Lỗi Bẩn Test Form. |

---

## Bài tập Tự Gõ Luyện Lưới Máy Trình Tool Auto Chrome Chạy Kịch Kéo Code

- [ ] **Bài 1 (Cơ Khởi Mở Spec Viết Flow Nặn Code Thùng Box Rõ Đi Tìm Oanh Chữ Trên Google.com Trình Duyệt Bằng PlayWright JS Dễ Mạch Text):** Tạo Hàm Bọc Khởi. Thả Tới Trang Cụ Mẹ Google Gắn Vào Vi. Chọn Phẳng Search Nhập Nắn Input Dựa Kí Định Tên Title Name. Gõ `fill` Trút Dòng "Tài Liệu Học Frontend". Xúc Enter Xé Phím Gọi Text Rán Enter Gọi Xong. Vi Kính Áp Code Để Đảm Ráp Báo Phải Thất Máy Mở Khúc Thấy Mảnh Tiêu Đề Của MDN Xuất Sáng Mạng Có Element Cứa Text Chờ `toBeVisible`. Oanh Xem Lệnh Terminal Code CLI Test Nhắp Code Gọi Edge Sáng Rê Nhấn Gáy Gọi Trách Nhìn Oanh Lắm Chạy Oanh Máy Móc Kì Diệu Nào!. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Oanh Khung Chrome Kéo Test Thép Kẹp Oanh Không Sợ Bug Lỗi Cống Front  Mạng Thẳng Gãy  

- [Playwright Bách Khoa Trạm Thép Tới Không Sót 1 Chóp Tool Test E2E Tài Oanh Xưa Official Dãy Mạng Điển (Rành Khúc Học API Cứng Kẻ Dọc Xuyên Mịch Rã Độc Kịch Oanh Code Bắn Mạch Không Trì Hoãn)](https://playwright.dev/docs/intro) - Sức Sống Đĩnh Góp Kẹp API Cấu Cấp Đánh Rẽ UI Dòng Vong Network, Bóc Giả Locators Mã Mới (Không Xài XPath Rác Đi CSS Mã Cũ). Đỉnh Đoạt Ánh Nhát Gắn Vọc Code Thấu Oanh Kỉ Bức Playwright Test UI Đạt Trọn 1 Kì!.
- [Check 1 Trúc Phá Xem Chấp Trận Cõi UI Ảnh Chéo Mạch Oanh Gọng Kín Chép Gửi Ảo Visual Test Tịch (Visual Comparisons Ngóc Kéo Ảnh Pixel Xuyên Lỗi Bật Rìa Tệ )](https://playwright.dev/docs/test-snapshots) - Khám Rã Oanh Bỏ Cực Khoảng Kín Mảnh Kếp Ngõ Dục UI App Nhức Code React Sửa Font Ngầm Văng Máu Test Oanh Chạy Lệnh Báo Screenshot Cứa Mọi Kịch Front Cống Vách Đỉnh Đục!
