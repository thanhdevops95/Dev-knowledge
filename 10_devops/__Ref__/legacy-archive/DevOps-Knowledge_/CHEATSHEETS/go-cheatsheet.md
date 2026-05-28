# Go Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Go syntax and commands for quick reference -- Cú pháp và lệnh Go để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [CLI Commands](#cli-commands) -- Lệnh CLI
- [Basics](#basics) -- Cơ bản
- [Data Types](#data-types) -- Kiểu Dữ liệu
- [Variables & Constants](#variables--constants) -- Biến và Hằng số
- [Strings](#strings) -- Chuỗi
- [Arrays & Slices](#arrays--slices) -- Mảng và Slices
- [Maps](#maps) -- Maps
- [Control Flow](#control-flow) -- Luồng Điều khiển
- [Functions](#functions) -- Hàm
- [Structs & Methods](#structs--methods) -- Structs và Methods
- [Interfaces](#interfaces) -- Interfaces
- [Error Handling](#error-handling) -- Xử lý Lỗi
- [Concurrency](#concurrency) -- Đồng thời
- [Packages & Modules](#packages--modules) -- Packages và Modules
- [Common Patterns](#common-patterns) -- Patterns Thường dùng

## <a id="cli-commands"></a> CLI Commands -- Lệnh CLI

```bash
# Run & Build -- Chạy và Build
go run main.go               # Run program -- Chạy chương trình
go run .                     # Run package -- Chạy package
go build                     # Build binary -- Build binary
go build -o myapp            # Build with name -- Build với tên
go install                   # Build and install -- Build và cài đặt

# Modules -- Modules
go mod init module_name      # Initialize module -- Khởi tạo module
go mod tidy                  # Clean dependencies -- Dọn dẹp dependencies
go mod download              # Download dependencies -- Tải dependencies
go mod verify                # Verify dependencies -- Xác minh dependencies
go mod vendor                # Create vendor directory -- Tạo thư mục vendor
go get package_name          # Add dependency -- Thêm dependency
go get -u                    # Update all dependencies -- Cập nhật tất cả dependencies
go get -u package_name       # Update specific dependency -- Cập nhật dependency cụ thể

# Testing -- Kiểm thử
go test                      # Run tests -- Chạy tests
go test ./...               # Run all tests -- Chạy tất cả tests
go test -v                  # Verbose output -- Output chi tiết
go test -cover              # With coverage -- Với coverage
go test -coverprofile=c.out # Coverage profile -- Profile coverage
go test -bench=.            # Run benchmarks -- Chạy benchmarks
go test -race               # Race detector -- Phát hiện race

# Other commands -- Các lệnh khác
go fmt ./...                # Format code -- Định dạng code
go vet ./...                # Analyze code -- Phân tích code
go doc package              # Show documentation -- Hiển thị tài liệu
go env                      # Show environment -- Hiển thị môi trường
go version                  # Show Go version -- Hiển thị phiên bản Go
go list -m all              # List all modules -- Liệt kê tất cả modules
```

## <a id="basics"></a> Basics -- Cơ bản

```go
// Package declaration -- Khai báo package
package main

// Imports -- Imports
import "fmt"
import (
    "fmt"
    "strings"
    "net/http"
)

// Main function -- Hàm main
func main() {
    fmt.Println("Hello, World!")
}

// Comments -- Chú thích
// Single line comment -- Chú thích một dòng
/*
Multi-line comment
-- Chú thích nhiều dòng
*/

// Printing -- In
fmt.Println("Hello")             // With newline -- Có xuống dòng
fmt.Print("Hello")               // Without newline -- Không xuống dòng
fmt.Printf("Name: %s\n", name)   // Formatted -- Định dạng
fmt.Sprintf("Name: %s", name)    // Return string -- Trả về chuỗi

// Format verbs -- Các verbs định dạng
%v   // Default format -- Định dạng mặc định
%+v  // With field names (structs) -- Với tên trường (structs)
%#v  // Go syntax representation -- Biểu diễn cú pháp Go
%T   // Type -- Kiểu
%d   // Integer -- Số nguyên
%f   // Float -- Số thực
%s   // String -- Chuỗi
%t   // Boolean -- Boolean
%p   // Pointer -- Con trỏ
%b   // Binary -- Nhị phân
%x   // Hexadecimal -- Thập lục phân
```

## <a id="data-types"></a> Data Types -- Kiểu Dữ liệu

```go
// Basic types -- Kiểu cơ bản
bool                          // Boolean: true, false
string                        // String -- Chuỗi

int   int8   int16   int32   int64    // Signed integers -- Số nguyên có dấu
uint  uint8  uint16  uint32  uint64   // Unsigned integers -- Số nguyên không dấu
byte                          // Alias for uint8 -- Bí danh cho uint8
rune                          // Alias for int32 (Unicode) -- Bí danh cho int32

float32  float64              // Floating point -- Số thực
complex64  complex128         // Complex numbers -- Số phức

// Zero values -- Giá trị zero
0       // Numbers -- Số
""      // String -- Chuỗi
false   // Boolean
nil     // Pointers, slices, maps, channels, functions, interfaces

// Type conversion -- Chuyển đổi kiểu
i := 42
f := float64(i)
s := string(i)                // Note: converts to rune -- Lưu ý: chuyển thành rune
s := strconv.Itoa(i)          // Int to string -- Int sang string
i, _ := strconv.Atoi(s)       // String to int -- String sang int
```

## <a id="variables--constants"></a> Variables & Constants -- Biến và Hằng số

```go
// Variable declaration -- Khai báo biến
var name string                    // Declaration -- Khai báo
var name string = "John"           // With value -- Với giá trị
var name = "John"                  // Type inference -- Suy luận kiểu
name := "John"                     // Short declaration -- Khai báo ngắn

// Multiple variables -- Nhiều biến
var a, b int
var a, b = 1, 2
a, b := 1, 2

// Variable block -- Khối biến
var (
    name    string = "John"
    age     int    = 25
    isAdmin bool   = true
)

// Constants -- Hằng số
const Pi = 3.14
const (
    StatusOK    = 200
    StatusError = 500
)

// Iota (for auto-incrementing) -- Iota (tự động tăng)
const (
    Monday = iota    // 0
    Tuesday          // 1
    Wednesday        // 2
)

const (
    _  = iota             // Skip 0 -- Bỏ qua 0
    KB = 1 << (10 * iota) // 1024
    MB                    // 1048576
    GB                    // 1073741824
)

// Pointers -- Con trỏ
var p *int                    // Pointer declaration -- Khai báo con trỏ
i := 42
p = &i                        // Get address -- Lấy địa chỉ
*p = 21                       // Dereference -- Truy cập giá trị
```

## <a id="strings"></a> Strings -- Chuỗi

```go
import "strings"

s := "Hello World"

// Basic operations -- Thao tác cơ bản
len(s)                            // Length -- Độ dài
s[0]                              // Byte at index -- Byte tại chỉ số
s[0:5]                            // Slice: "Hello" -- Cắt

// String methods -- Phương thức chuỗi
strings.ToUpper(s)                // "HELLO WORLD"
strings.ToLower(s)                // "hello world"
strings.TrimSpace(" hello ")      // "hello"
strings.Trim(s, "Hd")             // "ello Worl"
strings.Split(s, " ")             // ["Hello", "World"]
strings.Join([]string{"a","b"}, "-")  // "a-b"
strings.Contains(s, "World")      // true
strings.HasPrefix(s, "Hello")     // true
strings.HasSuffix(s, "World")     // true
strings.Index(s, "World")         // 6
strings.Replace(s, "World", "Go", 1)  // "Hello Go"
strings.ReplaceAll(s, "l", "L")   // "HeLLo WorLd"
strings.Count(s, "l")             // 3
strings.Repeat("Go", 3)           // "GoGoGo"

// String builder -- String builder
var sb strings.Builder
sb.WriteString("Hello")
sb.WriteString(" ")
sb.WriteString("World")
result := sb.String()             // "Hello World"

// String formatting -- Định dạng chuỗi
fmt.Sprintf("Name: %s, Age: %d", name, age)

// Runes -- Runes
r := []rune(s)                    // Convert to runes -- Chuyển sang runes
len([]rune(s))                    // Character count -- Số lượng ký tự

for i, r := range s {             // Iterate runes -- Lặp runes
    fmt.Printf("%d: %c\n", i, r)
}
```

## <a id="arrays--slices"></a> Arrays & Slices -- Mảng và Slices

```go
// Arrays (fixed size) -- Mảng (kích thước cố định)
var arr [5]int                    // Declaration -- Khai báo
arr := [5]int{1, 2, 3, 4, 5}      // Initialize -- Khởi tạo
arr := [...]int{1, 2, 3}          // Size inferred -- Kích thước suy luận
len(arr)                          // Length -- Độ dài

// Slices (dynamic) -- Slices (động)
var slice []int                   // Declaration -- Khai báo
slice := []int{1, 2, 3}           // Initialize -- Khởi tạo
slice := make([]int, 5)           // With length -- Với độ dài
slice := make([]int, 5, 10)       // Length and capacity -- Độ dài và dung lượng

// Slice operations -- Thao tác slice
len(slice)                        // Length -- Độ dài
cap(slice)                        // Capacity -- Dung lượng
slice[0]                          // Access -- Truy cập
slice[1:3]                        // Slice of slice -- Slice của slice
slice[:3]                         // First 3 -- 3 đầu tiên
slice[2:]                         // From index 2 -- Từ chỉ số 2

// Append -- Thêm vào
slice = append(slice, 4)          // Add one -- Thêm một
slice = append(slice, 4, 5, 6)    // Add multiple -- Thêm nhiều
slice = append(slice, other...)   // Add slice -- Thêm slice

// Copy -- Sao chép
dst := make([]int, len(src))
copy(dst, src)

// Delete element -- Xóa phần tử
slice = append(slice[:i], slice[i+1:]...)

// Iterate -- Lặp
for i := 0; i < len(slice); i++ {
    fmt.Println(slice[i])
}

for i, v := range slice {         // With index and value -- Với chỉ số và giá trị
    fmt.Printf("%d: %d\n", i, v)
}

for _, v := range slice {         // Value only -- Chỉ giá trị
    fmt.Println(v)
}
```

## <a id="maps"></a> Maps

```go
// Declaration -- Khai báo
var m map[string]int              // Nil map -- Map nil
m := make(map[string]int)         // Empty map -- Map rỗng
m := map[string]int{              // Initialize -- Khởi tạo
    "one": 1,
    "two": 2,
}

// Operations -- Thao tác
m["three"] = 3                    // Set value -- Đặt giá trị
value := m["one"]                 // Get value -- Lấy giá trị
value, ok := m["one"]             // Check exists -- Kiểm tra tồn tại
if !ok {
    // Key doesn't exist -- Key không tồn tại
}
delete(m, "one")                  // Delete -- Xóa
len(m)                            // Length -- Độ dài

// Iterate -- Lặp
for key, value := range m {
    fmt.Printf("%s: %d\n", key, value)
}

for key := range m {              // Keys only -- Chỉ keys
    fmt.Println(key)
}

// Check if key exists -- Kiểm tra key tồn tại
if value, ok := m["key"]; ok {
    fmt.Println(value)
}
```

## <a id="control-flow"></a> Control Flow -- Luồng Điều khiển

```go
// If-else
if x > 0 {
    fmt.Println("Positive")
} else if x < 0 {
    fmt.Println("Negative")
} else {
    fmt.Println("Zero")
}

// If with initialization -- If với khởi tạo
if v := getValue(); v > 10 {
    fmt.Println(v)
}

// Switch
switch day {
case "Monday":
    fmt.Println("Start of week")
case "Saturday", "Sunday":
    fmt.Println("Weekend")
default:
    fmt.Println("Weekday")
}

// Switch without expression -- Switch không có biểu thức
switch {
case x > 0:
    fmt.Println("Positive")
case x < 0:
    fmt.Println("Negative")
default:
    fmt.Println("Zero")
}

// Type switch -- Switch kiểu
switch v := i.(type) {
case int:
    fmt.Println("Integer:", v)
case string:
    fmt.Println("String:", v)
default:
    fmt.Println("Unknown type")
}

// For loop -- Vòng lặp for
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// While-style loop -- Vòng lặp kiểu while
for condition {
    // body
}

// Infinite loop -- Vòng lặp vô hạn
for {
    // body
    break  // Exit -- Thoát
}

// Range loop -- Vòng lặp range
for i, v := range slice {
    fmt.Printf("%d: %v\n", i, v)
}

// Loop control -- Điều khiển vòng lặp
break                             // Exit loop -- Thoát vòng lặp
continue                          // Skip iteration -- Bỏ qua vòng lặp

// Labels -- Nhãn
outer:
for i := 0; i < 10; i++ {
    for j := 0; j < 10; j++ {
        if condition {
            break outer           // Break outer loop -- Thoát vòng lặp ngoài
        }
    }
}
```

## <a id="functions"></a> Functions -- Hàm

```go
// Basic function -- Hàm cơ bản
func greet(name string) string {
    return "Hello, " + name
}

// Multiple parameters -- Nhiều tham số
func add(a, b int) int {
    return a + b
}

// Multiple return values -- Nhiều giá trị trả về
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Named return values -- Giá trị trả về có tên
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return  // Naked return -- Return trần
}

// Variadic function -- Hàm variadic
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
sum(1, 2, 3)                      // Call -- Gọi
sum(nums...)                      // Spread slice -- Trải slice

// Anonymous function -- Hàm ẩn danh
add := func(a, b int) int {
    return a + b
}

// Immediately invoked -- Gọi ngay
func() {
    fmt.Println("Hello")
}()

// Closure -- Closure
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

c := counter()
c()                               // 1
c()                               // 2

// Defer -- Defer
func main() {
    defer fmt.Println("End")      // Executed last -- Thực thi cuối
    fmt.Println("Start")
}

// Multiple defers (LIFO order) -- Nhiều defer (thứ tự LIFO)
defer fmt.Println("1")
defer fmt.Println("2")
defer fmt.Println("3")
// Output: 3, 2, 1
```

## <a id="structs--methods"></a> Structs & Methods -- Structs và Methods

```go
// Struct definition -- Định nghĩa struct
type Person struct {
    Name    string
    Age     int
    Address Address  // Nested struct -- Struct lồng nhau
}

type Address struct {
    City    string
    Country string
}

// Create struct -- Tạo struct
p := Person{Name: "John", Age: 25}
p := Person{"John", 25, Address{}}  // Positional -- Vị trí
p := new(Person)                    // Pointer to zero value -- Con trỏ đến giá trị zero
var p Person                        // Zero value -- Giá trị zero

// Access fields -- Truy cập trường
p.Name = "Jane"
fmt.Println(p.Name)

// Anonymous struct -- Struct ẩn danh
person := struct {
    Name string
    Age  int
}{
    Name: "John",
    Age:  25,
}

// Embedded struct -- Struct nhúng
type Employee struct {
    Person                          // Embedded -- Nhúng
    Company string
}
e := Employee{Person: Person{Name: "John"}, Company: "ACME"}
e.Name                              // Access embedded field -- Truy cập trường nhúng

// Methods -- Phương thức
func (p Person) Greet() string {
    return "Hello, " + p.Name
}

func (p *Person) Birthday() {       // Pointer receiver -- Receiver con trỏ
    p.Age++                         // Modifies original -- Sửa đổi bản gốc
}

// Call methods -- Gọi phương thức
p.Greet()
p.Birthday()

// Struct tags -- Tags struct
type User struct {
    Name string `json:"name" db:"user_name"`
    Age  int    `json:"age" db:"user_age"`
}
```

## <a id="interfaces"></a> Interfaces

```go
// Interface definition -- Định nghĩa interface
type Speaker interface {
    Speak() string
}

// Implementing interface -- Triển khai interface
type Dog struct {
    Name string
}

func (d Dog) Speak() string {
    return "Woof!"
}

// Using interface -- Sử dụng interface
var s Speaker = Dog{Name: "Buddy"}
s.Speak()

// Empty interface -- Interface rỗng
var any interface{}
any = 42
any = "hello"
any = []int{1, 2, 3}

// Type assertion -- Type assertion
value, ok := any.(string)
if ok {
    fmt.Println(value)
}

// Interface composition -- Kết hợp interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type ReadWriter interface {
    Reader
    Writer
}

// Common interfaces -- Các interface thường dùng
// io.Reader, io.Writer, io.Closer
// fmt.Stringer (String() string)
// error (Error() string)
```

## <a id="error-handling"></a> Error Handling -- Xử lý Lỗi

```go
// Return error -- Trả về error
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Handle error -- Xử lý error
result, err := divide(10, 0)
if err != nil {
    log.Fatal(err)
}

// Custom error -- Error tùy chỉnh
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Error wrapping (Go 1.13+) -- Bọc error
err := errors.New("original error")
wrapped := fmt.Errorf("context: %w", err)

// Unwrap error -- Mở bọc error
if errors.Is(wrapped, err) {
    fmt.Println("Match!")
}

var validationErr *ValidationError
if errors.As(err, &validationErr) {
    fmt.Println(validationErr.Field)
}

// Panic and recover -- Panic và recover
func mayPanic() {
    panic("something went wrong")
}

func safe() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered:", r)
        }
    }()
    mayPanic()
}
```

## <a id="concurrency"></a> Concurrency -- Đồng thời

```go
// Goroutine
go func() {
    fmt.Println("Running concurrently")
}()

go myFunction()                   // Run function -- Chạy hàm

// Channels -- Kênh
ch := make(chan int)              // Unbuffered channel -- Kênh không có buffer
ch := make(chan int, 10)          // Buffered channel -- Kênh có buffer

ch <- 42                          // Send -- Gửi
value := <-ch                     // Receive -- Nhận
close(ch)                         // Close channel -- Đóng kênh

// Range over channel -- Range trên channel
for v := range ch {
    fmt.Println(v)
}

// Select
select {
case v := <-ch1:
    fmt.Println("From ch1:", v)
case v := <-ch2:
    fmt.Println("From ch2:", v)
case <-time.After(time.Second):
    fmt.Println("Timeout")
default:
    fmt.Println("No message")
}

// WaitGroup
var wg sync.WaitGroup

for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(i int) {
        defer wg.Done()
        fmt.Println(i)
    }(i)
}
wg.Wait()                         // Wait for all -- Chờ tất cả

// Mutex
var mu sync.Mutex
var count int

func increment() {
    mu.Lock()
    defer mu.Unlock()
    count++
}

// RWMutex
var rwmu sync.RWMutex

func read() {
    rwmu.RLock()                  // Read lock -- Khóa đọc
    defer rwmu.RUnlock()
    fmt.Println(count)
}

func write() {
    rwmu.Lock()                   // Write lock -- Khóa ghi
    defer rwmu.Unlock()
    count++
}

// Once
var once sync.Once

once.Do(func() {
    fmt.Println("Only once")
})

// Context
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()

select {
case <-ctx.Done():
    fmt.Println("Timeout:", ctx.Err())
}
```

## <a id="packages--modules"></a> Packages & Modules -- Packages và Modules

```bash
# Initialize module -- Khởi tạo module
go mod init github.com/user/project

# go.mod file -- File go.mod
module github.com/user/project

go 1.21

require (
    github.com/gin-gonic/gin v1.9.0
)
```

```go
// Package structure -- Cấu trúc package
// myproject/
// ├── go.mod
// ├── main.go
// └── pkg/
//     └── mypackage/
//         └── mypackage.go

// mypackage.go
package mypackage

// Exported (public) -- Xuất (public)
func PublicFunction() {}

// Unexported (private) -- Không xuất (private)
func privateFunction() {}

// main.go
package main

import "github.com/user/project/pkg/mypackage"

func main() {
    mypackage.PublicFunction()
}

// Init function -- Hàm init
func init() {
    // Called before main -- Gọi trước main
}
```

## <a id="common-patterns"></a> Common Patterns -- Patterns Thường dùng

```go
// HTTP Server -- Server HTTP
package main

import (
    "encoding/json"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Hello, World!"))
    })
    
    http.HandleFunc("/json", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{"message": "Hello"})
    })
    
    http.ListenAndServe(":8080", nil)
}

// JSON encoding/decoding -- Mã hóa/giải mã JSON
type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

// Encode -- Mã hóa
p := Person{Name: "John", Age: 25}
jsonData, _ := json.Marshal(p)

// Decode -- Giải mã
var p Person
json.Unmarshal(jsonData, &p)

// File operations -- Thao tác file
// Read file -- Đọc file
data, err := os.ReadFile("file.txt")

// Write file -- Ghi file
os.WriteFile("file.txt", []byte("content"), 0644)

// Open file -- Mở file
file, err := os.Open("file.txt")
defer file.Close()

// Testing -- Kiểm thử
// mypackage_test.go
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Expected 5, got %d", result)
    }
}

// Table-driven tests -- Tests theo bảng
func TestAdd(t *testing.T) {
    tests := []struct {
        a, b, expected int
    }{
        {1, 2, 3},
        {0, 0, 0},
        {-1, 1, 0},
    }
    
    for _, tt := range tests {
        result := Add(tt.a, tt.b)
        if result != tt.expected {
            t.Errorf("Add(%d, %d) = %d, expected %d",
                tt.a, tt.b, result, tt.expected)
        }
    }
}

// Benchmark
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(1, 2)
    }
}
```

---
