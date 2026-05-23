# ♿ Accessibility (a11y) — Web cho mọi người

> `[INTERMEDIATE]` — Xây web ai cũng dùng được, kể cả người khuyết tật

---

## Tại sao Accessibility quan trọng?

**15% dân số thế giới** có khuyết tật — đó là **1 tỷ người**. Nếu web của bạn không accessible, bạn đang loại bỏ 15% users tiềm năng.

Nhưng a11y không chỉ cho người khuyết tật. Accessibility cải thiện UX cho TẤT CẢ users:

| Tình huống | Ai được lợi |
|---|---|
| Captions cho video | Người điếc + người xem ở nơi ồn + người học ngoại ngữ |
| Contrast cao | Người nhìn kém + người dùng ngoài nắng |
| Keyboard navigation | Người khiếm vận + power users (dev!) |
| Screen reader support | Người mù + người dùng assistive tech |
| Responsive text size | Người lớn tuổi + mobile users |

Ngoài ra, nhiều quốc gia có **luật bắt buộc** (ADA ở Mỹ, EN 301 549 ở EU). Không comply = rủi ro pháp lý.

---

## 1. Semantic HTML — Nền tảng quan trọng nhất

90% vấn đề a11y được fix bằng cách **dùng đúng HTML elements**. Screen readers đọc DOM tree — nếu bạn dùng `<div>` cho mọi thứ, nó không biết đâu là nút bấm, đâu là heading.

```html
<!-- ❌ "Div soup" — screen reader không hiểu gì -->
<div class="header">
    <div class="nav">
        <div class="link" onclick="goHome()">Home</div>
    </div>
</div>
<div class="main">
    <div class="title">Welcome</div>
    <div class="text">Content here</div>
</div>

<!-- ✅ Semantic HTML — screen reader hiểu cấu trúc trang -->
<header>
    <nav aria-label="Main navigation">
        <a href="/">Home</a>
    </nav>
</header>
<main>
    <h1>Welcome</h1>
    <p>Content here</p>
</main>
```

**Tại sao semantic quan trọng?** Screen reader thông báo:
- `<nav>` → "Navigation landmark"
- `<h1>` → "Heading level 1, Welcome"
- `<button>` → "Button, Submit" (+ có keyboard focus tự động!)
- `<div onclick>` → Không nói gì. User không biết nó clickable!

### Heading Hierarchy

```html
<!-- ❌ Skip levels — confusing for screen readers -->
<h1>Title</h1>
<h3>Subtitle</h3>  <!-- Nhảy từ h1 → h3? h2 ở đâu? -->
<h5>Detail</h5>

<!-- ✅ Sequential — logical structure -->
<h1>Welcome to Our Store</h1>
  <h2>Featured Products</h2>
    <h3>Electronics</h3>
    <h3>Clothing</h3>
  <h2>About Us</h2>
```

---

## 2. Images & Media

```html
<!-- ❌ Không alt → screen reader đọc filename hoặc bỏ qua -->
<img src="DSC_0042.jpg" />

<!-- ✅ Descriptive alt text — mô tả NỘI DUNG, không phải hình thức -->
<img src="team-photo.jpg" alt="Đội ngũ 5 người đang họp tại văn phòng, 
     nhìn vào laptop trên bàn" />

<!-- ✅ Decorative images: alt rỗng (screen reader bỏ qua) -->
<img src="decorative-line.svg" alt="" />

<!-- ✅ Complex images: dùng figure + figcaption -->
<figure>
    <img src="revenue-chart.png" alt="Biểu đồ doanh thu Q1-Q4 2025, 
         tăng từ 500M lên 800M" />
    <figcaption>Doanh thu tăng 60% trong năm 2025</figcaption>
</figure>

<!-- ✅ Video accessibility -->
<video controls>
    <source src="demo.mp4" type="video/mp4" />
    <track kind="captions" src="captions-vi.vtt" srclang="vi" label="Tiếng Việt" default />
    <track kind="captions" src="captions-en.vtt" srclang="en" label="English" />
</video>
```

---

## 3. Forms — Phần dễ sai nhất

```html
<!-- ❌ Input không label — screen reader đọc "edit text, blank" -->
<input type="email" placeholder="Enter email" />

<!-- ✅ Label liên kết input — screen reader đọc "Email, edit text" -->
<label for="email">Email</label>
<input id="email" type="email" placeholder="user@example.com" />

<!-- ✅ Error messages accessible -->
<label for="password">Mật khẩu</label>
<input 
    id="password" 
    type="password" 
    aria-describedby="password-error password-hint"
    aria-invalid="true"
/>
<p id="password-hint" class="hint">Tối thiểu 8 ký tự</p>
<p id="password-error" class="error" role="alert">
    Mật khẩu quá ngắn
</p>
<!-- aria-describedby: screen reader đọc hint + error khi focus input -->
<!-- role="alert": screen reader thông báo ngay khi error xuất hiện -->

<!-- ✅ Required fields -->
<label for="name">
    Họ tên <span aria-hidden="true">*</span>
    <span class="sr-only">(bắt buộc)</span>
</label>
<input id="name" type="text" required aria-required="true" />
```

---

## 4. Keyboard Navigation

Mọi interaction phải hoạt động **chỉ bằng bàn phím**:

```
Tab        → Di chuyển giữa interactive elements
Shift+Tab  → Di chuyển ngược
Enter      → Activate button/link
Space      → Toggle checkbox, activate button
Escape     → Đóng modal/dropdown
Arrow keys → Navigate trong menu, tabs, listbox
```

```html
<!-- ❌ Div không focus được bằng keyboard -->
<div class="card" onclick="selectCard()">Product</div>

<!-- ✅ Button: tự có keyboard support -->
<button class="card" onclick="selectCard()">Product</button>

<!-- ✅ Nếu PHẢI dùng div (custom component): thêm tabindex + keyboard handler -->
<div 
    class="card" 
    role="button" 
    tabindex="0"
    onclick="selectCard()" 
    onkeydown="if(event.key==='Enter') selectCard()"
>
    Product
</div>
```

### Focus Management cho Modals

```jsx
// Modal mở → focus vào modal, trap keyboard bên trong
function Modal({ isOpen, onClose, children }) {
    const modalRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            // Focus vào modal khi mở
            modalRef.current?.focus();

            // Trap focus: Tab chỉ cycle trong modal
            const focusable = modalRef.current.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            // ... implement focus trap
        }
    }, [isOpen]);

    return (
        <div 
            ref={modalRef}
            role="dialog" 
            aria-modal="true"
            aria-labelledby="modal-title"
            tabIndex={-1}
        >
            <h2 id="modal-title">Xác nhận</h2>
            {children}
            <button onClick={onClose}>Đóng</button>
        </div>
    );
}
```

---

## 5. ARIA — Khi HTML không đủ

ARIA (Accessible Rich Internet Applications) thêm thông tin cho screen readers khi custom components không có semantic HTML tương ứng:

```html
<!-- Tabs component -->
<div role="tablist" aria-label="Product tabs">
    <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
        Mô tả
    </button>
    <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
        Đánh giá
    </button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
    Nội dung mô tả...
</div>

<!-- Live region: thông báo thay đổi dynamic -->
<div aria-live="polite">
    <!-- Khi text thay đổi, screen reader đọc ngay -->
    Đã thêm vào giỏ hàng (3 sản phẩm)
</div>

<!-- Visually hidden text: chỉ screen reader đọc -->
<style>
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}
</style>
<button>
    <svg>...</svg>
    <span class="sr-only">Đóng menu</span>
</button>
```

**Rule #1 của ARIA**: Nếu có native HTML element → dùng nó. ARIA là **plan B**, không phải plan A.

---

## 6. Color & Contrast

```
WCAG Contrast Requirements:
  AA (minimum):  4.5:1 cho text thường, 3:1 cho text lớn
  AAA (enhanced): 7:1 cho text thường, 4.5:1 cho text lớn

❌ Light gray text (#999) on white (#fff) → ratio 2.85:1 FAIL
✅ Dark gray text (#595959) on white → ratio 7:1 PASS

Tool: Chrome DevTools → Elements → Styles → click color → xem contrast ratio
```

```css
/* ❌ Chỉ dùng màu để truyền đạt thông tin */
.error { color: red; }
.success { color: green; }

/* ✅ Thêm icon/text cùng với màu */
.error { color: red; }
.error::before { content: "❌ "; }
.success { color: green; }
.success::before { content: "✅ "; }
```

---

## Testing Checklist

```
Tools:
  ✅ Lighthouse (Chrome DevTools → Accessibility audit)
  ✅ axe DevTools (browser extension, chi tiết hơn Lighthouse)
  ✅ WAVE (web accessibility evaluator)
  ✅ Screen reader: NVDA (free, Windows), VoiceOver (Mac built-in)

Manual testing:
  ✅ Navigate toàn trang chỉ bằng keyboard (Tab, Enter, Escape)
  ✅ Zoom 200% — layout có bị vỡ không?
  ✅ Tắt CSS — content có đọc được theo thứ tự logic không?
  ✅ Thử screen reader: đọc qua 1 flow (login, checkout)
```

---

## Bài tập thực hành

- [ ] Audit 1 trang web bằng axe DevTools → fix top 5 issues
- [ ] Keyboard-only: navigate 1 trang web phức tạp chỉ bằng Tab/Enter
- [ ] Forms: thêm labels, errors, required fields accessible
- [ ] Screen reader: dùng VoiceOver/NVDA đọc 1 trang bạn build

---

## Tài nguyên thêm

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) — W3C standard
- [A11y Project](https://www.a11yproject.com/) — Practical checklist
- [Inclusive Components](https://inclusive-components.design/) — Pattern library
- [axe DevTools](https://www.deque.com/axe/devtools/) — Free testing tool
