# ⚡ Rust Concurrency & Async Deep Dive

> `[ADVANCED]` — Prerequisite: (Nắm vững vòng đời Ownership, mượn Borrowing) tại bài `01-rust-basics.md`.
> Sức mạnh độc tôn cốt lõi của Rust: Khả năng tính toán đa luồng và Asynchronous **KHÔNG SỢ DATA RACES** (Fearless Concurrency).

---

## 1. Cơ chế Hoạt động Bất đồng bộ (Async/Await) tại Rust

Nếu từng làm JavaScript/C#, khái niệm Async với bạn là "vùng chờ" gọi mạng. Tuy nhiên, Rust tiếp cận Async dưới một góc độ hoàn toàn khác. Ở JS, runtime chạy phía sau quản lý Promise. Ở C#, runtime quản lý Thread pool. Nhưng... Rust **không có Garbage Collector**, và **cũng chẳng có Runtime chạy ngầm định (Zero-cost abstractions)**!

```mermaid
graph TD
    A[Hàm Async Rust (Future)] -->|Biên dịch (Trình LLVM)| B(State Machine - Cỗ máy trạng thái State 1/2/3)
    B -.->|Không làm gì, Kẹt Cứng| C[Cần một Executor đẩy Bánh răng]
    D[Tokio / Async-std / Smol (Thư viện Executor Cắm Gửi)] -->|Cấp phát Theads, gọi .poll() liên tục| B
```

**Sự kiện cốt lõi (Lazy Futures):**
Trong JS, khi bạn gọi `fetch()`, lập tức code chạy nền lấy HTTP Request. 
Trong Rust, mọi thẻ "Future" (Promise kiểu Rust) đều **LƯỜI BIẾNG TUYỆT ĐỐI**. Hàm Async trả Future nhưng NÓ SẼ KHÔNG BAO GIỜ CHẠY NẾU BẠN KHÔNG GỌI lệnh `.await`. 

---

## 2. Kẻ Kích Hoạt (Executors) & Tokio

Bởi vì bản thân trình biên dịch thuần `rustc` không có Engine xử lý Network hay Pool Thread ngầm cho `Async/Await`, bạn bắt buộc phải kéo thêm 1 thư viện gọi là Executor. Tên tuổi đình đám thống trị là **`tokio`**.

```toml
# File: Cargo.toml
[dependencies]
tokio = { version = "1.37", features = ["full"] }
```

```rust
use tokio; // Kéo bộ thư viện vào RAM
use std::time::Duration;

// Hàm sẽ tự dịch Cỗ Máy State Machine lúc biên dịch.
async fn hello_world_later() {
    println!("Trải qua 2 giây!");
}

// Bắt buộc xài một vỉ Macro của Tokio để tạo Rễ Engine Async ở Hàm Main Nhánh 
#[tokio::main]
async fn main() {
    println!("Bắt đầu...");
    
    // Future mới nằm im Đợi Ngủ, Bóp `await` thì Tokio Executor kích đả hàm chạy vào 
    tokio::time::sleep(Duration::from_secs(2)).await; 
    
    hello_world_later().await;
}
```

---

## 3. Fearless Concurrency — Mutex, ARC & Channel

**Concurrency (Song song) có Data Races:** 
Khi 2 Threads (Luồng Hệ Điều Hành Cứng) cùng ghi đè Số Đếm (Counter) vào 1 Biến tại đúng 1 Mini-giây. RAM vỡ nát, Lỗi Logic Sinh. Các Ngôn ngữ Khác dính cả Rổ lỗi (Kể cả Go). Rust sẽ Quát bạn (Cấm biên dịch) nếu bạn làm vậy!

### Arc & Mutex (Gói Biến Chia Sẻ Xuyên Luồng)
Bạn cần chia sẻ trạng thái giữa 10 Thread của Tokio? Hãy nén Dữ liệu vào Mutex (Ổ khóa chống truy cập kép) rồi nén Lớp Vỏ Hươu Đếm Trỏ Vùng Nhớ `Arc` (Atomic Reference Counted - Nối Bắt RAM an toàn luồng).

```rust
use std::sync::{Arc, Mutex};
use tokio::task;

#[tokio::main]
async fn main() {
    // Ổ Khóa Ném 0 (Biến Tồn Tại Số). Bọc Hộp Đếm Reference An Toàn 
    let counter = Arc::new(Mutex::new(0)); 
    let mut tasks = vec![];

    for _ in 0..10 {
        // Clone Arc. Làm tăng số đếm Sở Hữu Counter tham lặp Nhớ RAM: 1->10 (Rõ Nét Ownership!).
        let counter_clone = Arc::clone(&counter);
        
        let handle = tokio::spawn(async move {
            // Khóa cửa Biến Đếm Lại. Chỉ 1 Thớt Sài Được Độc Quyền!
            let mut num = counter_clone.lock().unwrap(); 
            *num += 1;
            // Khóa tự Unlock Bật Khỏi Đoạn Mã Lúc End Khép `}` Này (Giọt Móc RAII Cực Đẹp!)
        });
        tasks.push(handle);
    }

    // Gôm Quét Chờ Đợi Đủ 10 Task Chạy Xong Nghỉ Phép
    for t in tasks { t.await.unwrap(); }

    // Kết Nối Bảo Toàn Tuyệt Đúng Trả Số 10. (In Lúc Trống Hêt Biến).
    println!("Số Tướng: {}", *counter.lock().unwrap());
}
```

### Channels (Ống Chuyển Giao / Message Passing)
Câu thần chú của cờ Concurrency: "Đừng nói chuyện bằng cách ghi đè bộ nhớ chung. Hãy chia sẻ vùng nhớ bằng cách Nói Chuyện qua ống giao Tín Hiệu (Channels)!"

- `mpsc`: Multiple Producer, Single Consumer. (Nhiều thằng Gửi Đẩy, Chỉ duy nhất Thằng Chủ được Đọc Ráp).

```rust
use tokio::sync::mpsc; // Dùng Channel Rất Nhẹ của Tokio Cấp Ống Async 

#[tokio::main]
async fn main() {
    // Kênh nạp Tối Đa 32 Tin Nhắn Ép Trong Ống Cúng. (Hữu Hạn Capacity Channel Tránh Mỏi Nổ RAM)
    let (tx, mut rx) = mpsc::channel(32); 

    let tx2 = tx.clone(); // Tạo Cái Vòi Bơm Tín Cầm 2 

    tokio::spawn(async move {
        // Gửi Gói Async Chờ Cho Chảy Đợi Vòi Trống Cốc
        tx.send("Báo Cáo 1 Tới!").await.unwrap();
    });

    tokio::spawn(async move {
        tx2.send("Báo Cáo 2 Tới!").await.unwrap();
    });

    // Màn Hứng Từng Gói Từ Đáy Cốc Gội Cùng. Vòng lặp tự Khóa Trạm Khi Ngắt (Tx cuối rụng).
    while let Some(message) = rx.recv().await {
        println!("Nhận Đài: {}", message);
    }
}
```

---

## 4. Performance Tuning / Production Tweak

1. **Hiểu Mức Thread Trội Ảo Tái Ráp (`join!` so với `.await` nhặt dọc):** Nếu bạn có 3 Future gọi Fetch API mạng ở cùng một thân Block, ĐIỀU RẤT KÉM CỞ LÀ Đợi Từng Cụ `.await` Nối Nhau Tuần Chờ (Tốn 3 Giây). Hãy ném chúng vào lệnh gộp đồng khởi Macro `tokio::join!(fet1, fet2, fet3)` Đón cả Trả Ráp 1Lượt (Tốn 1 Giây Do Chạy Song Luồng CPU Kép Non-Blocking).
2. **Loại Bể Gậy Kẹt Luồng Chết CPU `(Blocking Tasks)`:** Thư viện Code Crypto / Resize Hình Ảnh Đòi Nghiền CPU 100% Thuần Máy Cực Gắt? **Cấm Bỏ** nó vào lệnh Chạy Async Bình Thường (Sẽ Bể Toàn Diện Event Worker Khóa Mạch Thớt Của Tokio Mất Tốc). Hãy dùng Lệnh Ném Trúng Hàng Ngũ Kế Bị Văng Riêng: `tokio::task::spawn_blocking(|| { compute() })`.

---

## Gotchas — Bẫy Nên Chôn Rấp Phải Không Đốt Nhầm Trong Luồng

| # | ❌ Tư Duy Cũ Các Bảng Xếp JS/Go (Lỗi Chặn Vỡ Ống) | ✅ Rust Xử Kiể Bịch Kẹt Lỗi | Hậu quả của Việc Gắn Bệnh Nhặt Rác Ngôn Ngữ Khác |
|---|--------|---------|------------|
| 1 | Cứ Nhè Nối Async Lưới Dày Rằng `Result(X)` Chả Called Dữ Thường Hàng Chỗ Cho Bẫy Sạn Chờ (Như Chặn Promies JS Vô Sự Quên Chạy Async). | RUST Trạng Phanh Sáng Nhé. QUÊN Gọi Hàm Gắn  Phần `.await` Biển RUST Bắn Báo Compiler Cực Gớm Lỗ "Must Use Lập Trương". | Bỏ Cục Promise `Future` Mầm Im Ở Tầng Lửng Chẳng Thực Thi Phát Triển Đi Thậm Khủng Gọi Chặn Toàn Không Thấy Phép Hành Xử Gọi Rỗng Bug Nặng Logic. |
| 2 | Chứa Tranh Gắn Khóa `Std::sync::Mutex` Ở Giai Tầng Không Đồng Bộ Đạp Lệnh Wait Xoáy. | Lệnh Chứa Phải Nâng Sang `tokio::sync::Mutex` Nếu Bên Trọng Dây Đợi Nhả Lock Qua Đuổi Gọn Đám Lệnh `.await` Nhanh Lưới Nặng Chắn Thread Worker Mốc Gốc! | Luồng Chính Yếu Hệ Runtime Đứng Ngang Hình Tử Mạch Mất Giọt Hiệu Suất CPU Trống Trơn Khựng DeadLock Nhạc Nhéo Ngọn Chết Thảm Toàn App Đăng Ráp!. |
| 3 | Ngồi Vòng Tới Lui Quẹt Tạo Khỏi Sợi Vô Nghĩ `std::thread::spawn` Tốn Vài Răng MegaByte Giữa Chốt Kém Máy. | Async Của TOKIO Rụng Cho Gọi Giỏi `tokio::spawn` Nhiên Chấp Nó Rạch Giải Bỏ Hàm Triết Bịch Vài Kilobites Cho Mười Ngàn Ống Kết Luồng. | Phá Tụt Ram Nóng Khủng Khiếp Tải Đứt Hết Limit Mở Threads Nền OS Kernel Vỡ Đứt Connection Quá Tương App Game Quát Gây Liệt Chặn Vốn Không Cho Làm Máy Lạnh Bẩn Cặn. |

---

## Bài tập Tự Phá Khung Vững Đạt Song Tiến Concurrency Điểm Đáy Rust

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Đọc Future Non-Poll Lừa Lọc):** Viết Và Gọi Khung Định Async Nắm 1 Hàm Print. Không Gọi Lệnh Await Ở Xấp Hàm Main Main Khóa Rỗng Runtime Ở Rust. Dịch Nghĩ Báo Cáo Compile Đưa Coi Nhanh Thử Kín Có Chạy Qua Mặt In Chữ Gì Nào Không . 
- [ ] **Bài 2 (Trung bình Xới Lọc Dưới Channel Vòi):** Ôm Nặn Một Channel Phát Sóng Nhiều Gửi Rộng `tokio::sync::broadcast::channel()`. Tạo Tận 5 Tiến Con Kênh Nhỏ Chạy Nhờ Gọi Nút Thu `clone()`. Trút Rớt String Nhất Bắn Xuống `["Đã Vào Kho!"]`. Mở Cho 5 Vòng Trả Xuất Lời Receive Từng Receiver . Xem Tốp Luồng CPU Print Loạn Gõ Theo Giai Hóa Đoạc Cả Rừng  

---

## Tài nguyên Đọc Sâu Mở Khoá Hơn Thách Thức Ngôi Code Đẹp Khắc Sinh Lõi Rust

- [Đại Bách Khoa Cuốn Ngang Tuyển Của Đơn Lãnh Nhất Web Thế Giới Về Rust Async Sách Giấy Số 1 Async Book Gốc Mở](https://rust-lang.github.io/async-book/) - Nắm Cận Nghĩa Rõ Tới Giọt Vành Cơ Cấu Hoán Bật Của Rust Async Trạng Máy Xếp Đẩy Dịch Gọn . 
- [Tokio Trấn Phái Sách Khung Thực Tập (Tutorial Gốc Sạch Đẹp Ngỡ Như Giọt Code Vàng Của Core Team Cốt)](https://tokio.rs/tokio/tutorial) - Dò Giải Chặn Bản Kiến Web Thần Tô Không Rớt Bão Từ Lập Kế Thử Hướng Dữ Cận Thực Nhé Thục Kệnh Viết HTTP Bão Xoáy Hùng Hổ Lắp Đụng Xé Gốc.
