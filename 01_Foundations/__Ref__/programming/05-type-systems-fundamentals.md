# 🏷️ Hệ thống kiểu dữ liệu (Type Systems)

> `[INTERMEDIATE]` — Hiểu tại sao TypeScript tồn tại và khi nào cần kiểu mạnh

---

## Tại sao cần hiểu Type Systems?

```python
# Python — Chạy OK, nhưng lỗi lúc runtime!
def greet(name):
    return "Hello, " + name

greet("An")     # ✅ "Hello, An"
greet(42)       # 💥 TypeError: can only concatenate str
# Lỗi chỉ phát hiện khi chạy đến dòng đó!
```

```typescript
// TypeScript — Lỗi ngay khi viết code!
function greet(name: string): string {
    return "Hello, " + name;
}

greet("An");    // ✅ OK
greet(42);      // ❌ Compile error — Argument of type 'number'...
// Lỗi phát hiện TRƯỚC khi chạy → an toàn hơn!
```

---

## 1. Static vs Dynamic Typing

### Static — Kiểm tra kiểu **trước khi chạy** (compile time)

```
Code viết → Compiler kiểm tra kiểu → OK → Chạy
                                   → Lỗi → Không cho chạy!

Ngôn ngữ: Java, C, C++, Go, Rust, TypeScript, Kotlin
```

### Dynamic — Kiểm tra kiểu **lúc chạy** (runtime)

```
Code viết → Chạy luôn → Gặp lỗi kiểu → Crash lúc runtime!

Ngôn ngữ: Python, JavaScript, Ruby, PHP, Elixir
```

```python
# Dynamic: biến đổi kiểu tự do
x = 42          # x là int
x = "hello"     # x giờ là string — Python OK!
x = [1, 2, 3]   # x giờ là list — vẫn OK!
```

```java
// Static: kiểu cố định khi khai báo
int x = 42;
x = "hello";    // ❌ Compile error: incompatible types
```

---

## 2. Strong vs Weak Typing

### Strong — Không ngầm chuyển đổi kiểu

```python
# Python = Dynamic + Strong
"5" + 3        # ❌ TypeError — Python KHÔNG ngầm chuyển "5" → 5
int("5") + 3   # ✅ 8 — Bạn phải chuyển rõ ràng
```

### Weak — Ngầm chuyển đổi (type coercion)

```javascript
// JavaScript = Dynamic + Weak
"5" + 3        // "53"   — JS ngầm chuyển 3 → "3" rồi nối chuỗi
"5" - 3        // 2      — JS ngầm chuyển "5" → 5 rồi trừ
true + true    // 2      — true → 1
[] + {}        // "[object Object]"  — 😵 WTF JavaScript!
```

**Ma trận phân loại:**

```
           Strong (nghiêm ngặt)    Weak (lỏng lẻo)
          ┌─────────────────────┬────────────────────┐
Static    │ Java, Rust, Go,     │ C, C++             │
          │ Haskell, Kotlin     │ (void*, cast)      │
          ├─────────────────────┼────────────────────┤
Dynamic   │ Python, Ruby,       │ JavaScript, PHP,   │
          │ Elixir              │ Perl               │
          └─────────────────────┴────────────────────┘
```

---

## 3. Nominal vs Structural Typing

### Nominal — Phân biệt bằng **tên**

```java
// Java: 2 class cùng thuộc tính nhưng KHÁC kiểu
class Meter { double value; }
class Kilogram { double value; }

Meter distance = new Meter();
Kilogram weight = distance;  // ❌ Error! Khác tên class = khác kiểu
```

### Structural — Phân biệt bằng **cấu trúc** (duck typing)

```typescript
// TypeScript: "Nếu có cùng thuộc tính → cùng kiểu"
interface Point {
    x: number;
    y: number;
}

function printPoint(p: Point) {
    console.log(`(${p.x}, ${p.y})`);
}

const obj = { x: 10, y: 20, z: 30 };
printPoint(obj);  // ✅ OK! obj có x, y → tương thích Point
// Không cần "implements Point" — chỉ cần có đúng cấu trúc
```

**Duck Typing (Python):**

```python
# "Nếu nó đi như con vịt, kêu như con vịt → nó là con vịt"
class Dog:
    def speak(self): return "Gâu!"

class Cat:
    def speak(self): return "Meo!"

class Robot:
    def speak(self): return "Beep!"

# Không cần kế thừa từ cùng class — chỉ cần có method .speak()
def make_sound(animal):
    print(animal.speak())

make_sound(Dog())    # Gâu!
make_sound(Robot())  # Beep! — Robot cũng có .speak()
```

---

## 4. Type Inference — Suy luận kiểu

Compiler tự đoán kiểu — bạn không cần viết rõ:

```typescript
// TypeScript
const name = "An";           // Suy luận: string
const age = 25;              // Suy luận: number
const users = [name, "Bình"]; // Suy luận: string[]

// Không cần viết: const name: string = "An"
```

```go
// Go
x := 42              // Suy luận: int
y := 3.14            // Suy luận: float64
z := "hello"         // Suy luận: string
```

```rust
// Rust — suy luận rất mạnh
let numbers = vec![1, 2, 3];    // Vec<i32>
let doubled: Vec<_> = numbers.iter().map(|x| x * 2).collect();
// Rust tự suy luận _ là i32!
```

---

## 5. Generics — Kiểu tổng quát

Viết code hoạt động với **nhiều kiểu** mà vẫn an toàn:

```typescript
// ❌ Không generic: phải viết cho từng kiểu
function firstNumber(arr: number[]): number { return arr[0]; }
function firstString(arr: string[]): string { return arr[0]; }

// ✅ Generic: 1 hàm cho mọi kiểu
function first<T>(arr: T[]): T {
    return arr[0];
}

first([1, 2, 3]);        // T = number → trả về number
first(["a", "b", "c"]);  // T = string → trả về string
```

```python
# Python 3.12+ generics
from typing import TypeVar

T = TypeVar('T')

def first(items: list[T]) -> T:
    return items[0]

first([1, 2, 3])         # int
first(["a", "b", "c"])   # str
```

---

## 6. Type Annotations — Gợi ý kiểu

```python
# Python type hints (3.5+) — không bắt buộc, nhưng nên dùng
def calculate_total(
    items: list[dict],
    tax_rate: float = 0.1,
    discount: float | None = None,  # Python 3.10+ union type
) -> float:
    subtotal = sum(item["price"] for item in items)
    total = subtotal * (1 + tax_rate)
    if discount:
        total -= discount
    return total
```

**Lợi ích:** IDE autocomplete tốt hơn, bắt lỗi sớm với `mypy`, documentation tự động.

---

## So sánh Type Systems

| Ngôn ngữ | Static/Dynamic | Strong/Weak | Typing | Generics |
|---|---|---|---|---|
| **Python** | Dynamic | Strong | Duck | ✅ (hints) |
| **JavaScript** | Dynamic | Weak | Duck | ❌ |
| **TypeScript** | Static | Strong | Structural | ✅ |
| **Java** | Static | Strong | Nominal | ✅ |
| **Go** | Static | Strong | Structural | ✅ (1.18+) |
| **Rust** | Static | Strong | Nominal+Trait | ✅ |
| **C** | Static | Weak | Nominal | ❌ |

---

## Các lỗi thường gặp

```
❌ Sai: "Dynamic typing = không cần nghĩ về kiểu"
✅ Đúng: LUÔN nghĩ về kiểu — dùng type hints (Python) hoặc JSDoc (JS)

❌ Sai: Dùng `any` khắp nơi trong TypeScript
✅ Đúng: any = tắt type checking — dùng unknown hoặc generic thay thế

❌ Sai: "Static typing chậm development"
✅ Đúng: Tốn thời gian viết kiểu, nhưng tiết kiệm GẤP BỘI thời gian debug
```

---

## Bài tập thực hành

- [ ] Thêm type hints cho 1 file Python, rồi chạy `mypy` kiểm tra lỗi
- [ ] Viết generic function `Stack<T>` trong TypeScript (push, pop, peek)
- [ ] Liệt kê 5 JavaScript type coercion kỳ lạ (hint: `[] == false`)
- [ ] So sánh: viết cùng 1 function trong Python (no types) vs TypeScript (full types)

---

## Tài nguyên thêm

- [Type Systems 101](https://www.destroyallsoftware.com/compendium/types) — Giải thích cực hay
- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) — Tra cứu nhanh
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/) — Official
