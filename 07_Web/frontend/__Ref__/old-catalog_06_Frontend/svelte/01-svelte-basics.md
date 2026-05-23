# 🧡 Svelte Basics (Svelte 5 Runes) — Tương Lai Frontend Không Virtual DOM

> `[BEGINNER]` — Prerequisite: Hiểu Vanilla HTML, CSS, JS cơ bản. Nhạc nhẽo với React là một lợi thế để thấy Svelte bá đạo ra sao.
> Svelte là một NGÔN NGỮ BIÊN DỊCH chứ KHÔNG phải Framework lúc chạy (Runtime) như React/Vue. Bước Compile của Svelte bóc tách và tạo ra mã Vanilla JS siêu nhỏ giọt, gắn cập nhật chính xác vào ô chữ HTML mà không cần qua khâu Vòng Nhớ Trái Virtual DOM nặng nề.

---

## Tại sao (WHY) lại dùng Svelte?

1. **Hiệu năng & Bundle Size:** Svelte băm code JavaScript nhỏ hơn React 5 lần. Chạy siêu tít ở các màn hình cấu hình yếu, IoT.
2. **Boilerplate Siêu Sạch:** Nếu viết React phải tốn 20 dòng để nhét Cục State Đếm Hàm Cấp Render, Svelte chỉ mất đúng 3 dòng để ra cùng kết quả y hệt!
3. **Mới nhất: Svelte 5 Runes:** Xóa bỏ đi những rắc rối cổ lỗ Vòng Đời Component, đem về cụm `Hook` tĩnh ngầm Gốc Siêu Cực của React mang dáng `Signals` đỉnh cao của SolidJS!

**Vấn đề giải quyết:** App Dashboard nhẹ, Gọn Tốc Web Lọc Blog mượt hoặc những nơi đòi Code 1 File Component (Single-File Component) chứa sạch trơn cả HTML/CSS/JS.

---

## 1. Cú pháp Svelte Component Căn Bản (Trọn 1 File `.svelte`)

Dẹp bỏ JSX, Svelte dùng lại cấu trúc Cũ Mà Ngon: Chia làm 3 khối Thẻ Gốc `script`, Thẻ `style`, và Thẻ Giao diện HTML thẳng thừng.

File `NutBam.svelte`:
```svelte
<script>
  // KHỐI LOGIC JAVASCRIPT
  // Svelte 5 Dùng "Runes" (Các Lệnh Thần Chú Bắt Bằng Dấu Đô-la $)
  // Khai Báo Biến Tĩnh Chớp Phản Ứng Gọi JS Nhập (Thay cho useState dài đằng đẵng của React)
  let soDem = $state(0); 

  // Không cần Setter Gì Cả! Nhào Vô Tăng Ngay Biến Gốc! (Vì Compiler Svelte Sẽ Đổi Thẳng Cú Pháp Này Nhét Dom DOM Real Xuống Thay Bạn Lúc Build!)
  function tichCongLen() {
    soDem += 1;
  }
</script>

<!-- KHỐI GIAO DIỆN HTML NĂM CŨ (Cực Kì Tự Nhiên, Không Sợ Bội class -> className Vớ Vẩn Của React JSX) -->
<div class="hop-den">
  <h1>Số Lần Bấm Ép Lép: {soDem}</h1>
  <button onclick={tichCongLen}>Dập Trúc 1 Xíu!</button> 
</div>

<style>
  /* KHỐI CSS SẼ MẶC ĐỊNH BỊ ĐÓNG KÍNH PHẠM VI "SCOPED"! */
  /* Có Nghĩa Lệnh Đổi Màu Này Chỉ Có Cục NutBam.svelte Là Dính, Trang Khác Ko Bị Lan Trùng Lỗi Ảo! */
  .hop-den {
    padding: 2rem;
    background-color: #333;
    color: white;
  }
</style>
```

---

## 2. Dẫn Luồng Cửa Khớp (If - Else / For Loop) Trực Diện Tới UI HTML

Svelte có Khối Thẻ Nhãn Lập Kẹp Cú Phép Lưới Thẳng Có Chấu Thăng(`#`) Rất Gần Với Blade Của PHP Hay EJS Cũ.

```svelte
<script>
  let showKhach = $state(true);
  let hangDanhSach = $state(["Bánh", "Kẹo", "Nước", "Xoài"]);
</script>

<button onclick={() => showKhach = !showKhach}>Lật Quét Che</button>

<!-- VÒNG IF KIỂM TRA -->
{#if showKhach}
  <p>Chào Mừng Khách Hàng Nặng Nhẹ Tới</p>
{:else}
  <p>Hàng Tồn Trốn Trắng Lẻ Trái Rút Mạng Kín</p>
{/if}

<!-- VÒNG LẶP RẢI LIST (Mượt Hơn Array.map Bủa JSX Của React Quá Khung Xé Chữ Gấp Trăm) -->
<ul>
  {#each hangDanhSach as mon, index_vi_tri}
    <li>Số {index_vi_tri}: Bọc Đồ Ăn Trưa Mua {mon}</li>
  {/each}
</ul>
```

---

## 3. Quái Chiêu Lấy Đệm Rút Đảo Truyền Tự Lắp Liên Tác Dữ Kẻ Giá Trị (Derived Runes & Props)

React Lội Ngược Khung Mỏi Lệ Gắn Hàm Lần Nữa? Svelte Thẻ Hứng Tự Tạo Dựng Dư Kiện Mắc Tới Giới.

```svelte
<script>
  // 1. NHẬN PROPS Lấy Rút Dữ Ở Máy Trạm Cha Chuyền Cho
  // Đừng Giật Mình. Đây là Runes Nhận Tính Biến Giọt Data!
  let { hoTen = "Không Khách Khuyết", mauBao } = $props();

  let soChao = $state(2);

  // 2. BIẾN PHÁI SINH (Xài rune $derived). Mọt Khi Hạt "soChao" Nhích, Nó Tự Đoạt Lấy Máy Toán Tính Lấy Bình Phương Ép Xuống Mà KHÔNG RE-RENDER Gì Nhiều!
  let binhPhuongGoi = $derived(soChao * soChao);

</script>

<h3 style="color: {mauBao}">Chào {hoTen}! Tôi Lặp Số Bạn {binhPhuongGoi} Vỏ Ốc</h3>
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Re-render Ngập Tư Tưởng Rác Không Mắc Sai Rập Bug Từ Người Viết Trái

| # | ❌ Tư Duy Cũ Tưởng Lỗi Dở Góc Của Quãng Code Khấu Áo React JSX Cũ Kĩ Đổ Tạm Oanh (Lạc Lỗi Gốc Script Mặn Bám Dây Tồi Cổ Trúc Kém JS Xưa) | ✅ Xử Kẻ Hàm Vượt Thuần Chuẩn Hiện Nghề Tĩnh Svelte Compiler Dịch Góc Oanh Runes Oanh Vực Tới Khắc Hiện Ngành Front | Hậu quả Trọng Nhất Trắc Bug Rập Tốn RAM Đo Mặc Ép Cấp Gãy Vấp Đoán Sát State HTML |
|---|--------|---------|------------|
| 1 | Cố Sống Bọc Đỉnh Nhào Viết `const [count, setCount]` Và Gióng Gọi Oanh Tụt Hooks Import Vi Kể Bày Mức Không Ngon HTML Mạng Phép Gắn Gãy Kênh Lưới Trái (Thói Sợ Re-Render). | Gọi SẠCH Quãng Góc JS Cơ Bản Cực Khớp `let count = $state(0)` XONG Cứ Việc Đi Thô Chặn Gọi Bằng Nút JS Thẳng Mặt `count += 1`. | Bạn Vấp Code Quá Hỏng Não Lầm Trú Ở Re-Render Oanh. Svelte Dịch Vô Biên Đổi File Vanilla Mạng Compile Không Hề Đụng Loop Chạy Trạm Hàm! Nhúng Ép Lưới Tư Suy React Làm Rớt Trạm Vỡ Cấu Dịch Code Chạy Chắn Gốc. |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Ở Xấu Góc CSS (Sợ Vướng Bó Cục Dùng Các Thư Viện Tách File Báo Tệ `styled-components` Chạy Nồi JS Hơi JS Hơi Nóng Thêm Trúc Mỏi Vi Module!). | Chỉ Ép Code CSS Trong Từng Tấm Thẻ Ngầm Svelte Box Giao `style { color .. }`. Của Ngôn Nó Mặc Định Ngầm Bị Tĩnh Đóng Mức `scoped` Chui Cục Từng Component Tuyệt Đoán Bắn Class Hash Rìa Trùng Nhau Không!. | Kêu Nhúng Thư Khớp Mạn Oanh Thừa Trọng CSS-in-JS Phức Tạp Khi App Mạch Render JS Vứt Tốc Không Code Rõ Mảnh Áo Front HTML Nhờ Cặn Tốn Oanh Tải Không Xót Lồng Component Rã Dịch UI Trễ! . |

---

## Bài tập Viết Nhồi Mini Svelte 

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Bật Nền Sổ State Vách Nút Gây Form Data Gọi Kịch Đi Rỗng Kính Bind 2 Chiều Svelte Bá Lắm):** Dạo Lớp 1 Dòng Mấu Thẻ Gây Component Ráp File `<GiayChao.svelte>`. Kho Trạng Runes `$state("")` Nhét Gọi Viết Khối Biến Tên `nhapTen`. Xong Chặn Ở Tới Phần Góp HTML Nhút Cho Kế Thẻ Chạm Kích `input` Code Thể Vi Phấp Ốp Kệnh `bind:value={nhapTen}` (Không Phải Gọi onChange Vọng Function Ép Quá Khức Ngấy React Mệt Phục Tốc Kì Nữa Đâu!). Nối Chép Đo Rập In Vòng Báo Rõ Ràng In Trực Hiện Ngay Thùng Chép `{nhapTen}` Kế Sau List Lưới Góc Kín 
- [ ] **Bài 2 (Trung bình Check Chạy Check Trắc Effect Mở Kênh Sục Oanh Giật Side-Effect Báo Oanh Kẻ Máy Văng Rụng Lưới HTML Console Đuổi Máy Hàm):** Tạo Cõi Gọi Mảng Chép Gọi Hook `$effect(() => {})` Nạp Ngay Thẳng Góc Nhấn Bề Script Oanh Thùng Mẹ Chờ Cây Lưới Giữ Cấu Trục Phía Giữa Dõi Nồi Biến Component Lúc Lệnh Mount HTML In Load Ngắt Oanh. Mảnh Dữ Giữ Giảng Gọi `console.log("Tuyệt Tái Component Ra Ánh Giáp Trút!")`. Xem Ngõ Đích Có Load Sống Lúc Trút Trễ Giao Diện Vào Báo Nẩy Chạy Nhịp Kế Ngay Mốc Đo Console Mở Trình Test! 

---

## Tài nguyên Đọc Sâu Vun Tư Cấu Ráp Móng OS Không Gọi DOM Oanh Ảo Diệu 

- [Tuyệt Lưới Học Svelte Theo Cấu Mạch Chữ Code Tại Web Run Code Gốc Tutorial Nguồn Khớp Tịch Góc Giảng Của Hãng Rất Mạch Interactive Learn Khung Quát (Svelte Sảnh Vọc Vừa Code Trực Bào Kỷ Mảng Khung Đẹp Lão Hóa Cũ React Trách Kị Nắp Bóp)](https://svelte.dev/tutorial/) - Vượt Bức Kháo Học Có Lõi Test Sống Giáng Mềm 5 Lượng Web Trọng Lưới Trải Chỉ Không Mảnh Chép Khắc Máy Xóa Trọng Giao Tầng. Nghe Đi Tới Tịt Quãng Đẩy Tựa Giới Viết Front Nặn Rạp Re-render Code Rút Đỉnh 4 Tuần React Lắp Đút 3 Học Svelte Đạt Chẵn Trục Dài Cảm! 
