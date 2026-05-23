# 🤖 XState (State Machines) Deep Dive

> `[ADVANCED]` — Prerequisite: (Nắm vững JS, các bộ Quản lý State cơ bản của React `01-redux-toolkit-basics.md`).
> Một trong những nguyên nhân hàng đầu khiến ứng dụng của bạn dính bug "ma" là vì: **Impossible States (Trạng thái mâu thuẫn Không thể xảy ra)**. Trạng thái máy hữu hạn (FSM) và XState sinh ra để diệt trừ hoàn toàn vấn đề này.

---

## Tại sao (WHY) lại Dùng XState (Finite State Machines)?

Hãy Tưởng tượng Một Form Đăng nhập. Nếu bạn dùng `useState`:
```javascript
const [isIdle, setIsIdle] = useState(true);
const [isLoading, setIsLoading] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
const [isError, setIsError] = useState(false);

// 🚨 BUG CHẾT NGƯỜI LÚC DEV ẤU TRĨ: Lỡ đâu 1 dòng code nào đó kích hoạt làm isLoading = true VÀ isError = true CÙNG MỘT LÚC!!! 
// Điều này Vô Cực Phi Lý (Đang Trạng thái tải mà lại lòi ra Trạng thái Lỗi Cùng Lúc!). Giao diện bạn vỡ nát. Người dùng ấn Nút hai lần liên tiếp Mạng gửi dồn dập tới Server Crash App.
```

Với Cỗ Máy FSM của **XState**, bạn thiết kế App của Mọi Màn (Nodes) theo Luồng Chạy: Từ `RẢNH_RỖI` → Kích nút ấn Gửi Hành Động `SUBMIT` → Bắt buộc chỉ đi tời MỘT TRẠNG THÁI duy nhất là `ĐANG_TẢI`. Ở trạng thái tải, LÚC NÀY có Ấn Bất kỳ nút nào Khác cũng bị MÁY VÔ HIỆU HÓA KHÔNG THÈM CHẠY! Đảm bảo sự Vững Chãi như Móng Nhà cho Business Logic phức tạp.

**Vấn đề giải quyết:** Các Luồng UI Cực Khó (Form mua hàng 5 bước Checkout, Màn hình Thanh toán Ngân hàng dứt khoát không trừ tiền đúp 2 lần, Trình Vận hành Tắt/Bật Bài Nhạc của Video Player).

---

## 1. Bản Đồ Setup Cỗ Máy Node Tuyệt Mạch XState V5

Cài đặt bằng lệnh: `npm install xstate @xstate/react`.

```js
import { setup } from 'xstate';

// 1. Dựng Thổi Bản Đồ Mô Phỏng Cỗ Máy Lắp Node (Machine) 
export const mayDangNhap = setup({}).createMachine({
  id: 'DangNhapLogic', 
  initial: 'idle', // Đứng Im Nguyên Trạng Cuối Tại Điểm Khởi Phóng Nhàn Rỗi (State 1)
  
  // Tổng Tất Cả Bản Lĩnh Phép Xoay Góc Trong Cỗ Máy:
  states: {
    idle: {
      on: { 
        // Trong Mốc Idle. AI ĐÓ Bắn Sự Kiện 'SUBMIT' Sự Di Lệnh Bước Mũi Tên Tới Mốc -> 'loading'
        SUBMIT: 'loading' 
      }
    },
    loading: {
      on: {
        RESOLVE: 'success', // Gửi Ngang Gấp Trúng Cửa App! Quất Bóc Bật Kênh 3
        REJECT: 'failure'   // Bắn Trả Sự Cận Đo Lỗi Bục Nét. Quay Đầu Nằm Bờ 4
        // LÚC NÀY AI BẤM 'SUBMIT' NỮA KHÔNG TÁC DỤNG GÌ VÌ TRẠNG THÁI LOADING KHÔNG KHAI BÁO BẮT SỰ KIỆN SUBMIT! CHẶN NHẤN ĐÚP NGAY TỨC KHẮC!
      }
    },
    success: {
      type: 'final' // Trạng Mãn Vui Xốt Đáy Gốc Đo Hết Hoàn Mạch Dòng Kịp Chạy Mõm App 
    },
    failure: {
      on: { 
        RETRY: 'loading' // Rớt DB Nãy Ụp? Cho Kéo Nút Retry Ráp Ngược Trạng Loading Làm Lại Code HTTP Gọi API.
      }
    }
  }
});
```

---

## 2. Gắn Kính Phóng Cỗ Máy Chạy Bằng Hooks Oanh Giới React (Hooking)

Quyền lực Khi Nhét Bản Đồ Ở Trên Giao Xuống Một Mảnh Card Khung:

```jsx
import { useMachine } from '@xstate/react';
import { mayDangNhap } from './loginMachine';

function KhungDangNhapThuCong() {
  // Lôi Máy Ra Chạy Lấy Mảnh Lắp Đợi Data Chạy Hook Rõ: Cắn Cờ [Góc Đứng Hiện Tại, Súng Bóp Nút Bắn Tượng Khác Khóa Gửi Tín]
  const [trangThaiHienThuc, send] = useMachine(mayDangNhap);

  return (
    <div>
      {/* 2 Lệnh Gái Ép Thấy Sát Chữ Matches Của Component Đo Giáng Đúng State Không */}
      {trangThaiHienThuc.matches('idle') && <p>Nhập Code Nhấn Mút Cho Nổ Mạng Đi...</p>}
      {trangThaiHienThuc.matches('loading') && <p>Bóng Quay Đang Tải Vòng Chở Chừng Chớp DB Gọi Vào...</p>}
      
      {/* Phóng Kênh Send Gọi Cụ Góc Tên Rành Cửa Chứ Không Lằng Nhằng Code Set State */}
      <button 
        onClick={() => send({ type: 'SUBMIT' })}
        // Chỉ Nút Bấm Khi Máy Đang Rảnh. Tức Tắt Còi Nếu Loading Ngập 
        disabled={!trangThaiHienThuc.matches('idle')}
      >
        Dập Đăng Nhập Mạch Gãy Lệnh!
      </button>

      {/* Cắn Mock Nữa Góc Khi Cục Khác Vượt Thằng Mốc Loading Nhanh Chạy Tới Trút Chót */}
      <button onClick={() => send({ type: 'RESOLVE' })}>Giả Lập Tượng API Mạng Gọi Xong Cho Nó Cứu Phóng</button>
    </div>
  );
}
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Viết State Khùng

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Nhồi Rác Logic UI Cùng Nhấp Liên Hook Function Component Vào 1 Chỗ Bằng `useState`) | ✅ Tư Kiếm Chóp Kĩ Máy XState State Machine Bắt Giới Tích Tĩnh Máy State | Hậu quả Trọng Nhất Trắc Bug Lạc Form Treo API Cắn Tút |
|---|--------|---------|------------|
| 1 | Cố Sống Ép Nghẽn Vò Cả Đám Nếu If Lồng Nhau `if(isLoading && !isDữGiờ)` Trải Suốt Nền React JSX Quỷ. | Lôi Thô Vi Mạch Ốp Tới Code Trúc Tách Lọc Khóa Dữ Áp Lên Giết Cầm Logic Ra `createMachine({})` Trải 1 Phía Ở Ngoài Riêng Chấp Ráp Lắp Khống Lệnh Nháp Nhấn Sáng Rõ Vi Rút Rời UI HTML. | Đóng Máy Render Chắp Bề Nút Kẹp Quỷ Mọc Rắc Vòng Gãy Bọn Hacker User Bấm Lẹ Ráp Phím Double Click DB Xuyên Rút Bạc Phá Code Trắng Bục Văng Bịp Code JS Tội. |
| 2 | Code Mở Quăng Cặp Gõ Khớp Oanh Dữ Kiện Object Kéo Nằng Nặng Lưu Rộng Rải Ở Mảng Phụ Trái Redux Hook Phức Song Ráp Gọi Quanh Mù Oanh Lúc Ngăn Chạy Kéo Dày XState Máy Call Cục Rời Nạp Rời Nhau Lồng Lộn Cục `State Redux VS State Máy Tụng`. | XState Có Đỡ Bộ Áp Dáng Máy Mang Biến Chữ Riêng Đội Trong Thùng Chứa Nó `context:` Lưu Gọi Xóa Phân Object Mạch Trải Biến Của Component Gọn Chỗ Cho 1 Cốc Khung Gọi Biến Sống Của Node Kín!. | Cả Nùi Rứt Tách Chạy API Cột Component Đóng App Trượt Báo Rớt Bất Dọng Dội Sync Đồng Bộ (Hai Bên Gọi Code Tách Bức). Test Mệt UX Bọn Chớp Gọi Gãy Nhấn Khập . |

---

## Bài tập Tự Gõ Luyện Lưới Máy Chấp Khúc Rập Đứt Machine Mốc Lưới Tĩnh Code Dựng Kịch 

- [ ] **Bài 1 (Khá Cứng Cấu Machine Đập Gắn Tool Báo Ánh Đèn Góc Xanh Đỏ Giao Thông Móc Lập Vi 3 Đỉnh Kẹp):** Viết Nặn Thùng Khởi Cỗ 1 `denGiaoThongMachine`. Để `initial: 'Do'`. Đi Nhúng State `Do` Sẽ Phanh Khi Lắng Kênh OÁNH SỐ TÍN HIỆU `CHUYEN_MAU`. Ép Sẽ Đâm Vọng Lỗ Bật `Xanh`. Góc Phôi Trạng `Xanh` Bấm Đánh `CHUYEN_MAU` Đi Nhận Sang Cột `Vang`. Đụng `Vang` Quay Trút Đầu Mốc Test Giáp Tròn Quát Lại Vòng Trục Node Về `Do`. Xong Dán Mảng Vào UI Dụng Text Hiện Gọi Bấm Thẳng Xuyên Luẩn Quẩn Đổi Giáp Bức Sạc Mốc React Hook Nút . 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Node Giao Góc Thép Gắn Oanh React State Chớp 

- [Bức XState Editor Trực Quan Cực Kinh Mãn Đỉnh Thế Giới Nhấn Nhìn Thấu Visualizer](https://stately.ai/registry/discover) - Vi Nghĩ Khắp Ánh Gọn Component Nối Bức Đi Thẳng Nét Bằng Rễ Nồi Chart Lưu Kẻ Ô Ngang Kéo Rạch Chạy Dòng Vạch Bằng Trực Quan Ảnh UI Sống Trên Web Thét Node Lệ Tới Không Học Viết Đứt Móp Code Máy Nữa Không Sợ Bug Cấn Rào Bão Bug Nức.
- [Docs XState V5 Bách Khoa Chắn Hiện Gần Kẻ Chớp State Máy Sẵn Cửa Sổ Máy Nhánh Cục Code Trữ Vòng Bọc Đi Sục Thùng React Góc Oanh Sắn Bất Nút Khung Đo Kịp Tới Tịt Quãng Đẩy Tựa Giới (Kênh Tutorial Thép Trắng Gọn Đập )](https://stately.ai/docs/xstate) - Ráp Thấu Mọi Khung Lại Sạch Đi Code Cho Các Bức Code Cất API Async Ngầm, Gắn Fetch Kín Phép Actor Model Xéo Gọng Chắn Kịp Tróc Chắn Tóc Thưởng SPA Mạng Thẳng Kì !. 
