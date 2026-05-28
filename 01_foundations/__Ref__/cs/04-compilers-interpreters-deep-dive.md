# ⚙️ Compiler vs Interpreter — Từ code đến thực thi

> `[INTERMEDIATE → ADVANCED]` — Hiểu trình biên dịch và máy ảo hoạt động thế nào

---

## Tại sao cần học điều này?

- Tại sao C chạy nhanh hơn Python gấp 100 lần?
- JIT compilation là gì và tại sao JavaScript (V8) nhanh đến vậy?
- **Garbage Collector** nằm ở đâu trong kiến trúc?

Hiểu quá trình này giúp bạn chọn ngôn ngữ đúng và tối ưu hiệu năng.

---

## 1. Tổng quan: 3 con đường từ code → thực thi

```
Con đường 1: COMPILED (C, Go, Rust)
  Source code → [Compiler] → Machine code → CPU chạy trực tiếp
                                             ⚡ Cực nhanh

Con đường 2: INTERPRETED (Python cũ, Ruby, Bash)
  Source code → [Interpreter đọc từng dòng] → Thực thi
                                               🐌 Chậm

Con đường 3: HYBRID (Java, Python 3, JavaScript)
  Source code → [Compiler] → Bytecode → [VM/JIT] → Machine code
                                                    🚀 Khá nhanh
```

---

## 2. Quá trình biên dịch (Compilation Pipeline)

```
Source Code: "let x = 5 + 3 * 2"
       │
       ▼
┌─────────────┐
│ 1. LEXER    │  Tách thành tokens (từ vựng)
│ (Tokenizer) │  → [LET, IDENT(x), ASSIGN, NUM(5), PLUS, NUM(3), STAR, NUM(2)]
└──────┬──────┘
       ▼
┌─────────────┐
│ 2. PARSER   │  Xây dựng cây cú pháp (AST)
│             │  → LetDecl(x, Add(5, Mul(3, 2)))
└──────┬──────┘
       ▼
┌─────────────┐          ┌──────────┐
│ 3. SEMANTIC │  Kiểm tra │          │
│   ANALYSIS  │  kiểu,    │ Symbol   │  Bảng ký hiệu
│             │  scope    │ Table    │  (biến, hàm, kiểu)
└──────┬──────┘          └──────────┘
       ▼
┌─────────────┐
│ 4. IR GEN   │  Chuyển thành mã trung gian (Intermediate Representation)
│             │  → SSA, Three-address code
└──────┬──────┘
       ▼
┌─────────────┐
│5. OPTIMIZER │  Tối ưu: loại code chết, inline hàm, unroll vòng lặp
│             │  → Constant folding: 5 + 3*2 → 11 (tính sẵn!)
└──────┬──────┘
       ▼
┌─────────────┐
│ 6. CODE GEN │  Sinh mã máy cho CPU cụ thể (x86, ARM, RISC-V)
│             │  → mov rax, 11
└─────────────┘
```

### Lexer — Phân tích từ vựng

```
Input:  "if (x >= 10) { return true; }"

Tokens: [IF, LPAREN, IDENT(x), GTE, NUM(10), RPAREN, 
         LBRACE, RETURN, TRUE, SEMICOLON, RBRACE]
```

### Parser — Xây dựng AST

```
         IfStatement
        /          \
   Condition       Body
      |              |
  BinaryExpr     ReturnStmt
  /    |    \        |
IDENT  >=  NUM(10)  TRUE
 (x)
```

### Optimizer — Tối ưu code

```python
# Trước tối ưu
x = 5
y = 3
z = x + y   # Compiler biết x=5, y=3 → tính sẵn!

# Sau tối ưu (Constant Folding)
z = 8       # Không cần tính runtime!
```

---

## 3. Bytecode & Virtual Machine

Java và Python không compile thành machine code mà compile thành **bytecode** — chạy trên **máy ảo**:

```
Java:
  .java → [javac] → .class (bytecode) → [JVM] → Machine code

Python:
  .py → [CPython] → .pyc (bytecode) → [Python VM] → Thực thi

JavaScript:
  .js → [V8 Parser] → AST → [Ignition] → Bytecode → [TurboFan JIT] → Optimized code
```

**Tại sao bytecode?**
- **Portable:** Cùng bytecode chạy trên Windows, Linux, macOS
- **Tối ưu runtime:** JIT compiler quan sát hot paths → tối ưu đúng chỗ

---

## 4. JIT Compilation — Tốc độ của compiler, linh hoạt của interpreter

JIT (Just-In-Time) compilation = **compile lúc chạy**, chỉ compile code hay dùng:

```
JavaScript V8 Engine:

Source code
    │
    ▼
[Parser] → AST
    │
    ▼
[Ignition] → Bytecode (chạy ngay, chậm hơn)
    │
    │ Theo dõi: function nào gọi nhiều? (hot path)
    ▼
[TurboFan] → Optimized Machine Code (chỉ cho hot paths)
    │
    │ Nếu assumption sai? (deoptimize)
    ▼
Quay lại Bytecode
```

**Ví dụ:**

```javascript
// V8 theo dõi hàm này được gọi 10,000 lần
function add(a, b) {
    return a + b;
}

// Lần 1-100: chạy bytecode (chậm)
// Lần 101+: V8 thấy a, b luôn là number → JIT compile thành:
//   mov rax, [a]
//   add rax, [b]
//   ret
// → Nhanh gần bằng C!

// Nhưng nếu đột ngột: add("hello", "world")
// → Deoptimize! Quay lại bytecode
```

---

## 5. Garbage Collection (GC)

GC nằm trong **runtime** (VM), tự động giải phóng bộ nhớ:

```
┌─────────────────────────────────────────┐
│             Runtime Environment          │
│  ┌──────────┐  ┌───────────┐            │
│  │  VM /    │  │  Garbage  │            │
│  │ Runtime  │  │ Collector │            │
│  └──────────┘  └───────────┘            │
│  ┌──────────┐  ┌───────────┐            │
│  │  Memory  │  │ Standard  │            │
│  │ Manager  │  │ Library   │            │
│  └──────────┘  └───────────┘            │
└─────────────────────────────────────────┘
```

| Ngôn ngữ | GC Algorithm | Pause time |
|---|---|---|
| Java | G1GC (Generational) | Vài ms → hundreds ms |
| Go | Concurrent Mark-Sweep | < 1ms (rất ấn tượng!) |
| Python | Reference Counting + Cycle GC | Ngắn nhưng có GIL |
| JavaScript (V8) | Generational (Scavenger + Mark-Compact) | Vài ms |

---

## 6. So sánh tổng quan

| | Compiled | Interpreted | Hybrid (JIT) |
|---|---|---|---|
| **Tốc độ** | ⚡⚡⚡ | 🐌 | ⚡⚡ |
| **Startup** | Tốn thời gian compile | Chạy ngay | Nhanh, tối ưu dần |
| **Portability** | Phải compile lại cho mỗi OS | ✅ | ✅ (có VM) |
| **Debug** | Khó hơn | Dễ (từng dòng) | Trung bình |
| **Ví dụ** | C, C++, Go, Rust | Bash, old Ruby | Java, JS, Python, C# |

---

## 7. LLVM — Framework compiler hiện đại

**LLVM** là "backend" compiler được nhiều ngôn ngữ dùng chung:

```
Rust   ─┐
Swift  ─┤
C/C++  ─┤──► [Frontend] ──► LLVM IR ──► [LLVM Backend] ──► x86/ARM/WASM
Kotlin ─┤                                                   Machine Code
Zig    ─┘
```

> Mỗi ngôn ngữ chỉ cần viết **Frontend** (lexer + parser + semantic → LLVM IR). Backend tối ưu + code gen đã có LLVM lo!

---

## Các lỗi thường gặp

```
❌ Sai: "Python chậm vì interpreted"
✅ Đúng: CPython dùng bytecode + VM, có PyPy (JIT) nhanh gấp 10-100x

❌ Sai: "Compiled = luôn nhanh hơn"
✅ Đúng: JIT có thể nhanh hơn AOT vì tối ưu dựa trên runtime data

❌ Sai: "JavaScript chậm"
✅ Đúng: V8 JIT cực mạnh — JS performance gần C cho numeric computation
```

---

## Bài tập thực hành

- [ ] Dùng `dis` module Python: `import dis; dis.dis(lambda x: x + 1)` — xem bytecode
- [ ] Compile C với `-S` flag: `gcc -S hello.c` — xem assembly output
- [ ] So sánh time: Python vs PyPy vs Go cho cùng 1 bài toán (fibonacci, sort)
- [ ] Xem AST của JavaScript: [AST Explorer](https://astexplorer.net/)

---

## Tài nguyên thêm

- [Crafting Interpreters](https://craftinginterpreters.com/) — Free book, xây interpreter từ đầu
- [V8 Blog](https://v8.dev/blog) — Bên trong JavaScript engine
- [LLVM Tutorial](https://llvm.org/docs/tutorial/) — Viết ngôn ngữ mới dùng LLVM
