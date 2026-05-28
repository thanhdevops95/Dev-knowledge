# 🏎️ Go Performance Practices — Tối ưu Hiệu năng 

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `01-go-basics.md`, `02-go-concurrency-advanced.md`
> Những kinh nghiệm thực tiễn (Do's & Don'ts) để tối đa hoá tốc độ và tối thiểu hoá bộ nhớ trong các hệ thống Golang Production.

---

## 1. Bắt đầu với Profiling (Đo đạc trước khi làm)

Trong Go, đừng đoán. Hãy dùng `pprof` để định vị "nút thắt cổ chai" (bottleneck). Go cung cấp tool built-in mạnh bậc nhất.

**Cách 1: Gắn vào Web Server / API đang sống**
```go
import _ "net/http/pprof" // Chỉ cần import trắng để mount routes tự động

func main() {
    // pprof lúc này chạy ngầm ở http://localhost:8080/debug/pprof/
    http.ListenAndServe(":8080", nil) 
}
```

**Cách 2: Gắn vào các File chạy 1 lần (Batch script/CLI)**
```go
import "runtime/pprof"

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile() // Dừng ghi khi script hoàn tất
```

**Phân tích File (Terminal hoặc Web UI):**
```bash
go tool pprof cpu.prof          # Terminal
go tool pprof -http=:8081 cpu.prof # Web giao diện trực quan cực mạnh (FlameGraph)
```

---

## 2. Memory Size & Allocation (Bộ nhớ và Cấp phát)

Go là ngôn ngữ GC (Garbage Collection). Giảm số lần cấp phát (allocations) qua Heap sẽ làm giảm lượng công việc cho GC -> CPU Server sẽ rảnh rỗi hơn để phục vụ Request.

### ✅ Do: Pre-allocate (Khởi tạo sẵn độ dài Slice/Map)
Mỗi lần Slice vượt quá `capacity`, Go phải tạo Array mới to gấp đôi ở dưới C++ cấp và copy từng bytes qua. Việc này rất tốn Memory CPU.

```go
// ❌ Sai lầm (BAD): Khởi tạo mảng rỗng (0 capacity)
var users []User
for i := 0; i < 10000; i++ {
    users = append(users, User{ID: i}) // Gây ra ~14 lần copy toàn bộ dữ liệu!
}

// ✅ Chuẩn Production (GOOD): Biết trước Size
users := make([]User, 0, 10000) // Len 0, nhưng Capacity 10_000
for i := 0; i < 10000; i++ {
    users = append(users, User{ID: i}) // Không tốn một lần copy nào!
}
```

### ✅ Do: Tránh lạm dụng con trỏ (Pointer) bừa bãi
Trong C/C++, truyền con trỏ (truyền địa chỉ) cho Func thường để tiết kiệm chi phí "Clone object". Trong Go, **con trỏ được đánh dấu là dữ liệu "có khả năng tồn tại lâu", ép GC đẩy nó lên Heap Memory**. Garbage Collector "ghét" Heap.

Trái lại, nếu truyền bản sao (`User` thay vì `*User`), obj đó sẽ lưu ở **Stack**. Stack hoàn toàn **không tốn chi phí GC** (khi hàm chạy xong, stack tự sụp hủy sạch sành sanh với chi phí 0 ms). NẾU struct không quá to (< 10 MB), TỐT NHẤT HÃY TRUYỀN VALUE MẶC ĐỊNH.

```go
// ❌ Truyền bằng con trỏ khi không cần thiết (Tốn chi phí Heap/GC)
func process(u *User) int { return u.Age * 2 } 

// ✅ Truyền bằng Pass-by-Value (Tận dụng CPU Cache L1/L2 từ rễ Stack)
func process(u User) int { return u.Age * 2 }
```

---

## 3. Quản lý Concurrency (Goroutines / Channels)

Goroutine rẻ (~2KB Memory) NHƯNG nếu mở ra mà không bao giờ đóng (Goroutine Leak) → Server sẽ sập Memory (OOM - Out of Memory).

### ✅ Do: Luôn gắn Context Timeout cho MỌI Goroutines/APIs

```go
// Cha gọi Con, lỡ Thằng Con mất 10 phút để xử lý Database chưa xong? 
func handleRequest(w http.ResponseWriter, r *http.Request) {
    // Tự động giết Worker nếu Backend quá 3 giây chưa phản hồi
    ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second) 
    defer cancel() 
    
    // Gắn context chết chóc cho SQL Query
    db.QueryContext(ctx, "SELECT * FROM giant_table") 
}
```

### ✅ Do: Tái sử dụng Objects / Buffers 

Nếu bạn viết 1 API có tới 10_000 req/s, và ở mỗi request bạn tạo một struct Buffer json nặng nề -> Bạn sẽ nhanh chóng gặp CPU Spike (do GC chạy). Hãy dùng `sync.Pool`. Nó là cái giỏ đồ dùng chung tái chế cho tất cả Goroutines.

```go
var bufferPool = sync.Pool{
	New: func() any {
		return new(bytes.Buffer) // Chỉ tạo mới khi trong Giỏ chưa có
	},
}

func logMessage(msg string) {
    // Xin 1 cái Buffer Tái Chế
	buf := bufferPool.Get().(*bytes.Buffer)
	defer func() {
		buf.Reset() // Đổ rác đi trước khi vứt lại vào Pool
		bufferPool.Put(buf)
	}()
	
	buf.WriteString(msg)
}
```

---

## 4. Chuỗi / Strings (Immutable)

Kiểu `string` ở Go là CHỈ ĐỌC (giống Java/C#). Khi bạn Cộng 2 Chuỗi `a + b`, Go sẽ tạo 1 Object Chuỗi Thứ Ba Tách Biệt ở Vùng Mới -> Chi phí rất cao nếu nối >5 chuỗi trong Loop.

**✅ Do: Dùng `strings.Builder`**
```go
// ❌ Cực Chậm (O(N^2) memory)
var s string
for i := 0; i < 1000; i++ {
    s += "text" 
}

// ✅ Siêu Nhanh (O(N))
var builder strings.Builder
builder.Grow(4000) // Bí kíp: Tính trước Capacity
for i := 0; i < 1000; i++ {
    builder.WriteString("text")
}
return builder.String() // Lấy Chuỗi Ra
```

---

## Gotchas — Những lỗi làm "rớt hạng" System của bạn

| # | ❌ Sai (Lỗi Thường gặp) | ✅ Đúng (Performance Vượt Trội) | Hậu quả của Sai lầm |
|---|--------|---------|------------|
| 1 | Khai báo trường lớn trong file `struct` để trên cùng. | Sắp xếp trường (Fields) từ Nhỏ đến Lớn / hoặc Lớn nhất ưu tiên. | Struct bị **Padding (khoảng trắng)** bởi OS khiến size 1 Record to gấp rưỡi. Mất Data Locality Cache. |
| 2 | Nhồi tất cả JSON Response vào `json.Unmarshal(data, &obj)`. | Trực tiếp stream Decoder: `json.NewDecoder(req.Body).Decode(&obj)`. | Unmarshal ép bạn đọc sạch Payload sang Memory cục bộ. Decoder xài Stream Bytes nên Tốn ít RAM hơn rất nhiều. |
| 3 | Mở nhiều Goroutines ghi chéo dữ liệu vào một biến dùng `sync.Mutex` để lock. | Chỉ dùng `channels` để luân chuyển Data riêng rẽ, hoặc đổi dạng lock là `sync.RWMutex` | Toàn bộ các Cores CPU bị "tắc" tại 1 điểm Thắt Cổ Chai Lock (Lock Contention). |
| 4 | Dùng `fmt.Sprintf` để ghép URL hoặc chuỗi log | Hãy dùng Nối thẳng hoặc Log Format (e.g. Zap/Logrus) / `strconv.Itoa()` | `fmt.Sprintf` dùng Reflection đắt đỏ (Quét mọi Type của Input lúc chạy phần mềm). |

---

## Bài tập cải thiện thực tế

- [ ] **Bài 1 (Cẩn Thận):** Chạy lệnh Bench: Viết 1 file test dùng `testing.B` (`func BenchmarkStringConcat(b *testing.B)`). Làm và so sánh thời gian cộng mảng 10,000 chuỗi bằng `+` và bằng `strings.Builder`.
- [ ] **Bài 2 (Trung bình):** Tích hợp profiler Pprof vào 1 con REST API nho nhỏ 3 routes. Bắn tạ bằng tool `wrk` hoặc `hey` xem pprof vẽ Flame graph phần đỉnh ngọn lửa cháy ở đâu (Hàm nào ngốn CPU nhất).
- [ ] **Bài 3 (Khó):** Tạo con CLI parse 1 file Text 10 GB. Code một giải pháp dùng `bufio.Scanner` để không bị nổ Memory khi đọc, sau đó chèn Worker Pool (Goroutines = Số CPU Cores: `runtime.NumCPU()`) để phân loại chữ. So sánh xem nhanh hơn bao nhiêu lần so với code File truyền thống. 

---

## Tài nguyên thêm
- [Go Profiling Guide by DataDog](https://docs.datadoghq.com/tracing/profiler/) - Bách khoa toàn thư pprof từ hãng SRE nổi tiếng.
- [High Performance Go Workshop - Dave Cheney](https://dave.cheney.net/high-performance-go-workshop/dotgo-paris.html) - Khoá tài liệu tối mật cực hay bởi thiên tài Go Dave Cheney.
- [Visualizing memory management in Golang](https://deepu.tech/memory-management-in-golang/) - Sơ đồ giải thích Heap/Stack cực dễ hiểu. 
