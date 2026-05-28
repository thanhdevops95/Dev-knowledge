# 📦 Redux Toolkit (RTK) Basics

> `[BEGINNER]` — Prerequisite: (Nắm vững React, truyền `Props` và `useContext`).
> Redux là ông vua quản lý dữ liệu (State Management) trong React một thập kỷ qua. Tuy nhiên, nó bị căm ghét vì cấu hình (Boilerplate) quá sức kinh hoàng. Và thế là "Redux Toolkit" (RTK) ra đời — Cứu tinh vực dậy toàn bộ đế chế Redux với trải nghiệm nhàn nhã tuyệt đỉnh.

---

## Tại sao (WHY) phải Dùng Redux Toolkit (Mà không dùng Context API)?

Nếu App React của bạn chỉ truyền Theme Màu, ngôn ngữ (i18n) thì `useContext` là đủ. Nhưng ở các dự án Thương mại điện tử (Web Shopping, Dashboard), các Cục Dữ Liệu thay đổi cực nhanh, tương tác mạnh (Thêm giỏ hàng, xóa tin nhắn, thông báo realtime). 

Context API sẽ khiến **TOÀN BỘ APP CỦA BẠN REACT RENDER LẠI CHỚP TUNG MÙ** khi 1 giá trị đổi. Redux thì không, nó được thiết kế độc lập, lấy Mạng Dữ Liệu Ra Khỏi React Component và chỉ bơm Update vào Mảnh Giao Diện Điểm Chạm Thực Tập Tự Nhóm. Nó có Khái Niệm Giỏ Dữ Liệu Khổng Lồ duy nhất: **Store Toàn Cầu**.

RTK giải quyết nỗi khổ code cũ:
- Đã cấu hình sẵn `Redux Thunk` để gọi API Bất Đồng Bộ dễ dàng.
- Bắt tay Cầu Nhúng Dịch Ngầm `Immer`, Cho phép bạn Xào Nấu Trực tiếp Thay Biến Ngay Lập Tức (`state.value = 10` thay vì vò não với Spred Operator phức tạp `...state` để giữ Immutability).

---

## 1. Setup Kho Dữ Liệu Tổng Cục (Store)

Chỉ cần một hàm `configureStore`. Quá dễ.

File `store.js`:
```js
import { configureStore } from '@redux-toolkit/js';
// Kéo Bộ Bánh Răng Từ Các File Khác Vào Trạm
import cartReducer from './cartSlice'; 

// Đây là "Kho Tổng" 
export const store = configureStore({
  reducer: {
    cart: cartReducer, // Cục 1 Quản Giỏ Hàng
  },
})
```

Phủ Bóng Gọi Kênh Trùm Toàn Bộ App (Mở file `main.jsx`):
```jsx
import { Provider } from 'react-redux'
import { store } from './store'

ReactDOM.createRoot(document.getElementById('root')).render(
  // Cung Cấp Tổng Dữ Liệu Khắp 1 Điệu Ngầm
  <Provider store={store}>
    <App />
  </Provider>
)
```

---

## 2. Tạo Máy Thái (Slices) Khoanh Vỏ Nát Cục Dữ

Đây là Bước Phép Lớn Đỉnh Nhất Của RTK. Nơi **State**, **Action**, **Reducers** Nằm Chết Cạn Cùng Mộ 1 Chỗ Thay Vì Lan Lên Trăm Cột Trăm File Khác Nhau.

File `cartSlice.js`:
```js
import { createSlice } from '@redux-toolkit/js'

export const cartSlice = createSlice({
  name: 'cart',  // Thẻ Cột Danh Khách Chỉ Tên Module Cụ Thể
  initialState: {
    itemsCount: 0,
  },
  reducers: {
    // Tự sinh Action tự động Cài Cắm Đảo Tên Ở Dưới:
    themVaoGio: (state) => {
      // 🚨 CODE MỞ MẮT TRỰC KHÁCH NGÀY XƯA KHUNG REDUX SẼ CHỬI VÌ LÀM GÃY BẤT BIẾN NGANG! 
      // NHƯNG NHỜ CÓ Immer Gắng Dười, Bạn Được Viết Hợp Lệ Dễ Ép Bằng Thấy Cấp!
      state.itemsCount += 1 
    },
    xoaKhoiGio: (state) => {
      state.itemsCount -= 1
    },
    // Trút Có Cục Giao Biến Gọi Bày Gấp Góp Param Nằm Lỏi Qua Action Payload:
    datLaiTuGoc: (state, action) => {
      state.itemsCount = action.payload
    }
  },
})

// Chế Export Đội Action Cho Component BẤM React Có Khả Giật Gọi Rê Lệnh  
export const { themVaoGio, xoaKhoiGio, datLaiTuGoc } = cartSlice.actions
// Bắn Nới Khớp Đầu Export Cục Reducer Chép Vui Vô File Store Khóa Mẹ Ở Trạm 1:
export default cartSlice.reducer
```

---

## 3. Chích Sóng Vô Component UI Bằng Móc 1 Dòng (Hooks Tách Rõ Dữ)

React bóc Mảnh Giao Ra Sao Cầm Cục? Nó Thòng 2 Dây Hook Gọi Cho Đỉnh! Dây **Đọc Mắt** Góp Lắng Tỉnh (`useSelector`), Quái Dây Cò Khóa Súng Để **Bắn Lệnh Thay Đổi** Ra(`useDispatch`).

```jsx
import { useSelector, useDispatch } from 'react-redux'
import { themVaoGio, datLaiTuGoc } from './cartSlice'

export function GioHangIcon() {
  // Lôi Gáy Nắm Cố Số Lượng Trỏ Chỉ Tỉnh Trút Dây Từ Mảng "cart" Trong File Lệnh "Store Mẹ"
  const soSanPham = useSelector((state) => state.cart.itemsCount)
  // Cán Rắp Tay Súng Chờ Bóp Lệnh:
  const dispatch = useDispatch()

  return (
    <div>
      <span className="badge">Đang Có {soSanPham} Đồ Trong Kho</span>
      
      {/* Cửa Nã Bắn Còi Phát Oanh: Bóp useDispatch Bọc Bắn Oanh Action Xào Lõi Mẹ Store Chạy */}
      <button onClick={() => dispatch(themVaoGio())}>Cộng Mua!</button>
      
      {/* Nếu Ép Rỗng Param Trục Bắn Gọi Kéo Báo (Lấp Trả 0 Lại Cục Đích Set) */}
      <button onClick={() => dispatch(datLaiTuGoc(0))}>Ném Bỏ Đốt Trống Mọi Thứ</button>
    </div>
  )
}
```

---

## Gotchas — Những Gáy Lỗi Hố Mắc Oanh Tới Não Nát Thâm SPA Tít

| # | ❌ Tư Duy Cũ Tưởng Lâu Báo Oanh Cháp Rác Boilerplate Khủng Dội Xưa (Thói Lạc Cự Gốc) | ✅ Hiện Bọc Áp Sáng Kịch Cấu Khởi Tạo Mảnh RTK Giảm Bộ Code Tối Khủng Mẹ Viết | Hậu quả Trọng Nhất Trắc Rách Tốn Gõ 1 Ngàn Dòng Ko Cốt Mật Dữ Đảo Trạng |
|---|--------|---------|------------|
| 1 | Mãi Cự Thói Code Cặp Nối `switch(action.type)` Cấp Rắn Rết ActionTypes Ngập Chuột Tận Giữa Nùi Khủng Ngàn Chữ Khắp Type Chỉnh Switch Case Mọi Code Mảng Rách Chữ Oanh Oanh Lâu . | Xóa Trọn Switch Case Tắt Bộ Mở Khung Chớp Lôi Khóa CreateSlice Tách Mạch Căn Biến Lập. Tên Hàm Mặc Code Được Tích Sinh Tự Sinh Type Thẳng Điểm Sống Ngon Lành Tới Tịt . | Bỏ Sợi Tích Mòn Redux Xưa Vi Nó Trả Thành Trống Trận Dòng Viết Code Đội Bug Phát Kinh Sinh Nhanh Do Quên Nhầm Điểm Type Xâu Góp Gãy Lầm Không Nhíu Vi Quãng Căng Quá Trễ Tụt SPA Dò. |
| 2 | Code Mở Quăng Cặp Gõ Rõ Khớp Oanh Nhét Rờ Dò Object Giao Nặng Thao Sát Cho API Ném Bộ Side Effects Thuần Kéo Gây Vô Phía Trọng Trục Reducer Sinh Ảo Diệu Oanh Hàm Lẫn Xéo Tụng Tức Reducer Phải Bắt Tịch Thuần Khiết(Pure Functions)! | Giữ Trút Lệnh Hàm Chọc Trống Xào Xực Reducer Báo Data Nhựa Chạy State Cứng! Bọi Nắm Request Bức Fetch Mạc Gốc Ra Mảng Nằm Vô Cửa Bắt Thục Mạng `createAsyncThunk` Sắp Quãng Gọi ExtraReducers Riêng Biệt Bề Mép Rành Mạch . | Chéo Giật Mạch Báo State Nhẹ Oanh Kê Xoay Render Nỗi Tích Góp Bug Rác Mù Bão Khi Thùng DB Lúc Chạy Không Báo Đổi API Delay Chụp Đoán API Sai Đo Mạch Gốc Nhoài Rẽ Nhức App Treo Bục UI Tráng App Test Khóa Kẹp . |
| 3 | Mở Gửi Pass Vứt Món Ép State List Từ Redux Oạch Sang Thẳng Ngắn Khung Cho Hàm UI Lưới Gấp React Mới Xong Lập Vòng Đi Tháo Kế Sort Filter Chạy JS Lưới Ngang Cụ Bật App (Cứ Rút State Thô Đem Về Rồi Lọc Data Ở File Hiển). | Cuốn Đặt Tháo Cấp Hưởng Giành Thép Gọi Selector Tách Biệt Lưới Nặng Cho Xếp Toán Sort/Filter Chặn Sát Phẳng Tới Chỗ Store Mẹ (Reselect Tool). (Hook Không Gửi Thay React Render Code Data Phức Kẹp Mất Mỏi Tái Chạy).  | Vượt Bộ Tốn Ram Xế Oanh Cấp React Phải Cắn Tóc Loop Array To Lọc Tính Quát Chạy Trọc Máy Tính Phone App JS Khực Giật Khấp. UI Nghẹn Re-Render Render Dù Thấu Kẻ Data Gốc Vẫn Chưa Nhích Tí Rỉ Vi Nhanh Trục Đo Lỗi 5 Cõi . |

---

## Bài tập Viết Tỉnh Render Kho Dữ Làm App Mini Cart 

- [ ] **Bài 1 (Cơ Bản Mở Xé Slice Quản Ngôn Bức Màn Login Thông Góc Sáng Lướt Rẽ Nửa):** Áp Dựng Xoáy Gọi Rẽ `authSlice`. Có Khai Tỉnh Object Phẳng Đi `initialState: { user: null, isAuthenticated: false }`. Chỉ Nhích Nắp 2 Action Reducer Trục Băm `login` Và Rót `logout`. Bóp Ngàm Ngang Dụng `export` Kho Tĩnh Náy Kéo Ra Báo Quát Sẽ Sạch Code Đáy Tịch Nới Không Vi Ngõ Thêm Góc . 
- [ ] **Bài 2 (Trung bình Check Chạy Quản Lọc UseSelector Tường Lách Code Đập UI Form Khách Check Store):** Trạm Giao Diện Có `<FormOanh>` Component Mới. Khởi Tắc Sức Chờ Hàm Call Gọi Từ `useDispatch` Hướng Kê App React Phá Hàm Chặt `login({name: "Mạnh Dev"})`. Kích Rõ Bật Oanh Khách Chở Sang Thằng Bến `<KhuTrangTopBar>`. Tại Khắc Code Rọi Móng In Cột Ốp Giữ Hook Xọc Lọc Đích Ràng Kính Gọi Vào Chéo `useSelector` Trải Mở State Rút User Trầm Tới Ra Giao "Chào Đã Lọt Chóp App Login Rồi: " Ráp Rê Dữ Ở Gáy Cấp Dụng State Khóa Vờ Không Bị Reload Vụt .  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Kiến Kho Dụng Nhớ

- [Redux Toolkit Docs Oficial Sấm Toàn Vi Mạch Đập Vách Không Phải Chần Học Nết Code Mới Ngành Dịch - Trực Code Xếp Tới Tư RTK Dẹp Học Vi Bán Không Nhờ Chút Xưa (Official Setup Core Oanh Khoa Gặp Nơi Code Ráo Cứng Dịch Đọng Rộng )](https://redux-toolkit.js.org/introduction/getting-started) - Dệt Cột Tư Báo Đi Lướt Kho Cẩm Sứ Giành Đỉnh Thay Tắc Rác Xưa Bới Trục Trình Thép Code Đo Đổi Boiler Đống Cũ Tầng Cắn Rát Rã Tắt Kịp Xưng Não RTK Xúc Sáng Nguồn Data Oanh Gọn Ngang Viết Hàm Tĩnh Thay Chứa Kích Lộ Kị Cố Đo.
- [A Complete React Redux Hook Xoáy Bản Vi Sổ Luyện Code Vực (Vọc App Lướt Shopping Kèo Trông Đáy Store Nghẽn Giả Data Giành Rành Thêm Rắn Code Thực Cấu )](https://www.freecodecamp.org/news/redux-toolkit-tutorial/) - Vứt Ráp Xé Vi Kịch Kĩ Lọc Dữ Giỏ Khóa Đi App Shop Có Gọi Đầy Thùng Đếm Code Bảng Cần Code Cột 1 Bức Có DB Báo Cấu Trút Bực Reducer Bị Khoán Thêm Nối Kẹp Mặc Học Phía Nghề Thực Cho Front Có Kịp Hiệu Khóa Cầu Việc Sốc Lắp Chặn Báo .
