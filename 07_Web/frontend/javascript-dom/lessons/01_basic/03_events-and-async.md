# 🎓 Events & Async — Click, Promise, async/await

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [DOM Manipulation](02_dom-manipulation.md)

> 🎯 *Master events: **`addEventListener`** + 20+ event types, **bubbling + delegation**, **`preventDefault`/`stopPropagation`**. Plus async: **`setTimeout`/`setInterval`**, **Promise**, **`async/await`** + error handling. Sau bài này write JS interactive đầy đủ.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng **`addEventListener`** thay `onclick=` cũ
- [ ] Master 20+ event types (`click`, `submit`, `input`, `keydown`, `scroll`...)
- [ ] Hiểu **bubbling + capturing** + **event delegation** (efficient)
- [ ] **`preventDefault`** vs **`stopPropagation`** — khi nào dùng
- [ ] **`setTimeout`/`setInterval`** + cancel
- [ ] **Promise** — create + chain + error
- [ ] **`async/await`** — modern syntax, try/catch
- [ ] **`Promise.all`/`Promise.race`** — concurrent

---

## Tình huống — Bạn làm filter sản phẩm, performance kém

Bạn làm list 1000 sản phẩm, mỗi sản phẩm có button "Add". Bạn viết:

```javascript
document.querySelectorAll('.product .add-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    // ... add to cart
  });
});
```

→ 1000 listener — tốn memory + chậm. Mới thêm sản phẩm chưa attach listener.

Bạn muốn:
- Fetch products mỗi 30 giây refresh
- Click search → debounce 300ms trước fetch
- Multiple fetch parallel
- Handle network error

Bạn thử callback hell:
```javascript
fetch('/products', (products) => {
  fetch('/categories', (categories) => {
    fetch('/users', (users) => {
      // 4 level nest 😱
    });
  });
});
```

Senior chỉ:
> *"3 bug + 1 anti-pattern. Học **delegation** (1 listener thay 1000), **`async/await`** (thay callback hell), **debounce** (efficient input)."*

→ Bài này dạy events + async đầy đủ.

---

## 1️⃣ `addEventListener` — Modern way

### Cơ bản

`addEventListener` là API chuẩn 2026 để **lắng nghe event** trên element. Nhận 2 argument: event name (string) + handler function. Handler tự động nhận `event` object chứa info về sự kiện:

```javascript
const btn = document.querySelector('#myBtn');

btn.addEventListener('click', () => {
  console.log('Clicked');
});

// With event object
btn.addEventListener('click', (event) => {
  console.log(event.target);      // → button element
  console.log(event.type);         // → "click"
  event.preventDefault();           // prevent default action
});
```

### vs Cũ `onclick="..."`

Trước `addEventListener` (~2000), JS chỉ có `onclick` attribute hoặc property. Bảng dưới so sánh 4 hạn chế của cách cũ — đặc biệt **không support multiple listener** là deal-breaker:

| Aspect | `onclick=""` (inline / property) | `addEventListener` |
|---|---|---|
| Multiple listener | ❌ Override | ✅ Stack |
| Remove listener | Hard | `removeEventListener(...)` |
| Options (capture, once, passive) | ❌ | ✅ |
| Modern | ❌ | ✅ |

→ **Default 2026**: `addEventListener`.

### Remove listener — Phải reference

Để remove listener, **phải pass cùng function reference** đã dùng khi add. Anonymous function (`() => {}`) không remove được — vì mỗi lần viết là 1 reference khác. Pitfall phổ biến với React/Vue cleanup:

```javascript
function handleClick() { console.log('Clicked'); }

btn.addEventListener('click', handleClick);
btn.removeEventListener('click', handleClick);    // OK — same reference

// ❌ KHÔNG remove được anonymous
btn.addEventListener('click', () => console.log('x'));
btn.removeEventListener('click', () => console.log('x'));    // FAIL — different fn ref
```

→ Cần remove → **named function** hoặc lưu reference.

### Options

`addEventListener` nhận object option ở argument thứ 3 — control thêm 4 hành vi: auto-remove sau 1 lần fire, phase capture vs bubble, passive cho scroll perf, signal để cancel batch:

```javascript
btn.addEventListener('click', handler, {
  once: true,         // Auto remove sau lần đầu fire
  capture: false,     // Default — bubbling phase
  passive: true,      // Promise won't preventDefault (perf scroll/touch)
  signal: abortController.signal    // Cancel via AbortController
});
```

### AbortController — Cancel multiple listeners

`AbortController` là API hiện đại để **cancel batch listener cùng lúc** — gọi `controller.abort()` là tất cả listener có chung signal đều remove. Pattern này dùng nhiều trong React `useEffect` cleanup:

```javascript
const controller = new AbortController();

btn.addEventListener('click', handler1, { signal: controller.signal });
input.addEventListener('input', handler2, { signal: controller.signal });

controller.abort();    // Cancel cả 2
```

→ Pattern modern cho cleanup (React useEffect).

---

## 2️⃣ Event types — 20+ phổ biến

### Mouse

```javascript
el.addEventListener('click', ...)         // Click chuột trái
el.addEventListener('dblclick', ...)      // Double click
el.addEventListener('contextmenu', ...)   // Right click
el.addEventListener('mouseenter', ...)    // Vào element
el.addEventListener('mouseleave', ...)    // Ra element
el.addEventListener('mousemove', ...)     // Di chuột (perf!)
el.addEventListener('mousedown'/'mouseup', ...)
el.addEventListener('wheel', ...)          // Scroll wheel
```

### Keyboard

```javascript
el.addEventListener('keydown', e => {
  console.log(e.key);             // "a", "Enter", "ArrowUp", ...
  console.log(e.code);             // "KeyA", "Enter", "ArrowUp", ...
  console.log(e.ctrlKey, e.shiftKey, e.altKey, e.metaKey);
});
el.addEventListener('keyup', ...)
el.addEventListener('keypress', ...)      // Deprecated, dùng keydown
```

→ `e.key` recommended (logical), `e.code` cho game (physical key).

### Form / Input

```javascript
input.addEventListener('input', e => {     // Mỗi keystroke
  console.log(e.target.value);
});
input.addEventListener('change', ...)      // Khi blur + value đổi
input.addEventListener('focus', ...)
input.addEventListener('blur', ...)
form.addEventListener('submit', e => {
  e.preventDefault();                       // Prevent reload
  // Handle submit
});
```

### Touch (mobile)

```javascript
el.addEventListener('touchstart', ...)
el.addEventListener('touchmove', ...)
el.addEventListener('touchend', ...)
```

### Window / Document

```javascript
window.addEventListener('load', ...)              // After all resources
window.addEventListener('DOMContentLoaded', ...)   // HTML parsed
window.addEventListener('resize', ...)
window.addEventListener('scroll', ...)
window.addEventListener('beforeunload', e => {     // Warn before close
  e.preventDefault();
  e.returnValue = '';
});
window.addEventListener('online'/'offline', ...)
window.addEventListener('hashchange', ...)         // URL # change
window.addEventListener('popstate', ...)            // history.back/forward
```

### Custom events

```javascript
// Dispatch
const event = new CustomEvent('cart-updated', {
  detail: { items: 3 }
});
window.dispatchEvent(event);

// Listen
window.addEventListener('cart-updated', e => {
  console.log(e.detail.items);    // 3
});
```

→ Hữu ích cho component-component communication.

---

## 3️⃣ Event object — Properties

```javascript
btn.addEventListener('click', event => {
  event.target          // Element clicked (deepest)
  event.currentTarget   // Element listener attached (= btn)
  event.type             // "click"
  event.timeStamp        // ms since page load
  event.bubbles          // true if bubbles
  event.cancelable        // true if preventDefault works

  event.clientX, event.clientY        // Mouse position viewport
  event.pageX, event.pageY            // Mouse position page (with scroll)
  event.offsetX, event.offsetY        // Relative to element

  event.preventDefault();              // Cancel default browser action
  event.stopPropagation();              // Stop bubbling/capturing
  event.stopImmediatePropagation();     // + cancel other listeners on same element
});
```

### `target` vs `currentTarget`

```html
<div id="parent">
  <button id="child">Click me</button>
</div>
```

```javascript
document.querySelector('#parent').addEventListener('click', event => {
  console.log(event.target);          // button (deepest)
  console.log(event.currentTarget);   // div (listener attached here)
});
```

→ `target` quan trọng cho **event delegation** (§5).

---

## 4️⃣ `preventDefault` vs `stopPropagation`

### `preventDefault()` — Cancel default browser action

```javascript
// Submit form không reload
form.addEventListener('submit', e => {
  e.preventDefault();
  // Handle JS
});

// Link không navigate
a.addEventListener('click', e => {
  e.preventDefault();
  console.log('Custom action');
});

// Checkbox không toggle
checkbox.addEventListener('click', e => {
  if (locked) e.preventDefault();
});
```

### `stopPropagation()` — Stop bubble up

```html
<div id="outer" onclick="alert('outer')">
  <div id="inner">Click me</div>
</div>
```

```javascript
document.querySelector('#inner').addEventListener('click', e => {
  console.log('inner clicked');
  e.stopPropagation();     // Outer KHÔNG nhận event
});
```

→ Dùng khi không muốn parent handler trigger.

### Khác nhau

| | preventDefault | stopPropagation |
|---|---|---|
| Tác dụng | Cancel browser default | Stop event bubbling |
| Ví dụ | Submit form, navigate link | Outer onclick |
| Có thể combine | ✅ | ✅ |

---

## 5️⃣ Event bubbling + Delegation

### Bubbling — Event đi từ target → root

```html
<body>
  <div>
    <button>Click</button>
  </div>
</body>
```

Click button:
```
button click
  ↓ bubble
  div click
    ↓ bubble
    body click
      ↓ bubble
      document click
```

→ 3 listener attach → cả 3 fire.

### Capturing — Ngược lại (ít dùng)

```javascript
parent.addEventListener('click', handler, { capture: true });
// Fire trước child
```

### **Event Delegation** — Pattern quan trọng

Thay vì attach 1000 listener trên 1000 button, attach **1 listener** trên parent:

```html
<ul id="list">
  <li class="item" data-id="1">Item 1</li>
  <li class="item" data-id="2">Item 2</li>
  <li class="item" data-id="3">Item 3</li>
  <!-- ... 1000 items ... -->
</ul>
```

```javascript
// ❌ 1000 listener
document.querySelectorAll('.item').forEach(item => {
  item.addEventListener('click', () => {
    console.log(item.dataset.id);
  });
});

// ✅ 1 listener với delegation
document.querySelector('#list').addEventListener('click', event => {
  const item = event.target.closest('.item');
  if (!item) return;          // Click ngoài item, ignore

  console.log(item.dataset.id);
});
```

### `closest(selector)` — Đi lên tree tìm parent match

```javascript
event.target.closest('.btn-primary')    // Trả ancestor (hoặc self) match
                                          // null nếu không có
```

→ Magic của delegation. Click trên child của `.item` (vd `<span>` bên trong) vẫn detect được.

### Pros delegation

- ✅ **Memory** — 1 listener vs 1000.
- ✅ **Dynamic** — element mới thêm sau cũng work (không cần re-attach).
- ✅ **Code clean** — handle 1 chỗ.

→ **Modern best practice** cho list, table dynamic.

---

## 6️⃣ `setTimeout` / `setInterval` — Time-based

### `setTimeout`

```javascript
const id = setTimeout(() => {
  console.log('Sau 2 giây');
}, 2000);

// Cancel trước khi fire
clearTimeout(id);
```

### `setInterval`

```javascript
const id = setInterval(() => {
  console.log('Mỗi giây');
}, 1000);

// Cancel
clearInterval(id);
```

### Debounce — Wait trước khi action (search input)

```javascript
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

const search = debounce(query => {
  console.log('Searching:', query);
  // fetch(...)
}, 300);

input.addEventListener('input', e => search(e.target.value));
// User gõ "h", "he", "hel", "hell", "hello" → chỉ search "hello" sau 300ms
```

### Throttle — Limit rate (scroll handler)

```javascript
function throttle(fn, limit) {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall < limit) return;
    lastCall = now;
    fn(...args);
  };
}

window.addEventListener('scroll', throttle(() => {
  console.log('Scroll');
}, 100));
// Chỉ fire mỗi 100ms tối đa
```

→ Debounce + throttle là **must-know** cho performance.

---

## 7️⃣ Promise — Modern async

### Create Promise

```javascript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    const success = Math.random() > 0.5;
    if (success) {
      resolve('OK');
    } else {
      reject(new Error('Fail'));
    }
  }, 1000);
});
```

### Use Promise — `.then` / `.catch` / `.finally`

```javascript
promise
  .then(value => console.log('Got:', value))
  .catch(err => console.error('Err:', err))
  .finally(() => console.log('Done'));
```

### Chain

```javascript
fetch('/users')
  .then(res => res.json())               // Promise → Promise
  .then(users => users[0])                // value → value
  .then(user => console.log(user))
  .catch(err => console.error(err));
```

→ Mỗi `.then` return value (hoặc Promise) cho `.then` kế tiếp.

### Promise states

```
PENDING  → FULFILLED  (resolve)
PENDING  → REJECTED   (reject)
```

→ Settled (xong) = fulfilled hoặc rejected. Không quay lại pending.

### `Promise.all` — Wait tất cả

```javascript
const [users, posts, comments] = await Promise.all([
  fetch('/users').then(r => r.json()),
  fetch('/posts').then(r => r.json()),
  fetch('/comments').then(r => r.json()),
]);
// Chạy parallel, đợi tất cả xong. 1 fail = tất cả fail.
```

### `Promise.allSettled` — Wait tất cả, không fail nếu 1 reject

```javascript
const results = await Promise.allSettled([p1, p2, p3]);
// Result: [{status: "fulfilled", value: ...}, {status: "rejected", reason: ...}, ...]
```

### `Promise.race` — First settled

```javascript
const result = await Promise.race([
  fetch('/api'),
  new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 5000))
]);
// Whichever finishes first
```

→ Pattern timeout cho fetch.

---

## 8️⃣ `async/await` — Sugar trên Promise

### Cơ bản

```javascript
async function loadUser() {
  const res = await fetch('/users/1');
  const user = await res.json();
  return user;          // Auto-wrapped trong Promise
}

// Call
loadUser().then(user => console.log(user));

// Hoặc
(async () => {
  const user = await loadUser();
  console.log(user);
})();
```

→ Code đọc như **sync**, nhưng vẫn async.

### Error handling — `try/catch`

```javascript
async function loadUser() {
  try {
    const res = await fetch('/users/1');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Failed:', err);
    return null;
  } finally {
    console.log('Always run');
  }
}
```

### Parallel với `Promise.all`

```javascript
// ❌ Sequential — chậm
const user = await fetch('/users/1').then(r => r.json());
const posts = await fetch('/users/1/posts').then(r => r.json());
const comments = await fetch('/users/1/comments').then(r => r.json());
// Total: 3 × RTT

// ✅ Parallel — nhanh hơn 3x
const [user, posts, comments] = await Promise.all([
  fetch('/users/1').then(r => r.json()),
  fetch('/users/1/posts').then(r => r.json()),
  fetch('/users/1/comments').then(r => r.json())
]);
// Total: max(3 × RTT)
```

→ Always `Promise.all` khi parallel.

### Top-level await (ES modules)

```javascript
// In ES module file
const data = await fetch('/api').then(r => r.json());
// OK trong module, không cần wrap async function
```

→ Modern modules support top-level `await`.

---

## 9️⃣ Bạn viết app modern

```javascript
// search.js
const input = document.querySelector('#search');
const list = document.querySelector('#results');

// Debounced search
const search = debounce(async (query) => {
  if (!query) {
    list.innerHTML = '';
    return;
  }

  try {
    list.textContent = 'Loading...';
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const products = await res.json();

    list.innerHTML = '';
    products.forEach(p => {
      const li = document.createElement('li');
      li.textContent = `${p.name} — ${p.price.toLocaleString()}đ`;
      list.append(li);
    });
  } catch (err) {
    list.textContent = `Error: ${err.message}`;
  }
}, 300);

input.addEventListener('input', e => search(e.target.value));

// Event delegation — click any product
list.addEventListener('click', e => {
  const li = e.target.closest('li');
  if (!li) return;
  console.log('Clicked:', li.textContent);
});

function debounce(fn, delay) {
  let id;
  return (...args) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), delay);
  };
}
```

→ Search debounced + async fetch + error handle + delegation. Modern + performant.

---

## ⚠️ 5 pitfall hay vướng

1. **Quên `e.preventDefault()` cho form submit** → page reload, mất data. Always có khi handle bằng JS.
2. **Anonymous listener không remove được** → cleanup leak. Dùng named function hoặc AbortController.
3. **`setInterval` không clear** → multiple interval chồng → app crash. Always `clearInterval` khi unmount/leave page.
4. **`await` trong loop sequential** → chậm. Dùng `Promise.all` cho parallel:
   ```javascript
   // ❌ for (const id of ids) await fetch('/users/' + id)
   // ✅ await Promise.all(ids.map(id => fetch('/users/' + id)))
   ```
5. **Quên `try/catch` async** → Unhandled Promise Rejection. Always wrap.

---

## ✅ Self-check

1. `addEventListener` vs `onclick=""` — chọn cái nào, vì sao?
2. **Event delegation** giải quyết vấn đề gì?
3. Khác **`preventDefault`** và **`stopPropagation`**?
4. **Debounce** vs **throttle** — khác nhau, use case?
5. `Promise.all` vs `Promise.allSettled` — khi nào dùng cái nào?

<details>
<summary>Gợi ý đáp án</summary>

1. **`addEventListener`** — modern, multiple listener stack, options (`once`, `signal`...), remove được. **`onclick=""`** legacy, override khi assign mới, không options. **2026 dùng `addEventListener`**.

2. **Vấn đề**: 1000 element = 1000 listener → tốn memory + element mới thêm sau không có listener. **Delegation**: 1 listener parent, check `event.target.closest(sel)` để detect target. Pros: less memory, dynamic content auto-work.

3. **`preventDefault()`** = cancel default browser action (form submit → reload, link click → navigate). **`stopPropagation()`** = chặn event bubble lên ancestor (outer onclick không fire). Combine được.

4. **Debounce** = đợi user **stop** activity trong N ms rồi fire 1 lần. Dùng cho search input (chỉ search sau khi gõ xong). **Throttle** = fire **tối đa 1 lần / N ms**. Dùng cho scroll/resize (limit rate).

5. **`Promise.all`** — chờ tất cả OK, **1 fail = tất cả reject**. Dùng khi cần ALL succeed (load page data). **`Promise.allSettled`** — chờ tất cả settled, không fail. Trả result array với status. Dùng khi muốn biết kết quả tất cả (partial success OK).
</details>

---

## ⚡ Cheatsheet

### Event basics

```javascript
el.addEventListener('click', e => { ... });
el.removeEventListener('click', fn);   // Need same ref
el.addEventListener('click', fn, { once: true, signal });
```

### Event types

```
Mouse:  click  dblclick  contextmenu  mouseenter/leave  wheel
Key:    keydown  keyup
Form:   input  change  submit  focus  blur
Touch:  touchstart  touchmove  touchend
Window: load  DOMContentLoaded  resize  scroll  beforeunload
```

### Delegation

```javascript
parent.addEventListener('click', e => {
  const el = e.target.closest('.item');
  if (!el) return;
  // handle
});
```

### Async patterns

```javascript
// Promise
fetch(url)
  .then(r => r.json())
  .then(data => ...)
  .catch(err => ...);

// async/await
try {
  const r = await fetch(url);
  const data = await r.json();
} catch (err) { ... }

// Parallel
const [a, b] = await Promise.all([p1, p2]);

// Timeout
Promise.race([fetch(url), timeoutPromise(5000)]);
```

### Debounce/throttle

```javascript
const debounced = debounce(fn, 300);    // wait stop
const throttled = throttle(fn, 100);    // max 1/100ms
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Event** | Action xảy ra (click, scroll, load, ...) |
| **Listener / Handler** | Function chạy khi event fire |
| **`addEventListener`** | Modern method attach handler |
| **Event object** | Data về event (target, type, ...) |
| **Bubbling** | Event đi từ target lên root |
| **Capturing** | Ngược lại — root xuống target |
| **Delegation** | 1 listener parent thay nhiều children |
| **`preventDefault`** | Cancel browser default |
| **`stopPropagation`** | Stop bubble |
| **Debounce** | Đợi stop trước khi fire |
| **Throttle** | Limit rate fire |
| **Promise** | Object async — pending/fulfilled/rejected |
| **`async`/`await`** | Sugar trên Promise |
| **`Promise.all`/`allSettled`/`race`** | Combine multiple promises |
| **AbortController** | Cancel listeners / fetch |

---

## 🔗 Links

### Trong cluster
- ← Trước: [DOM Manipulation](02_dom-manipulation.md)
- → Tiếp: [Fetch API & Modules](04_fetch-and-modules.md)
- ↑ Cluster: [javascript-dom README](../../README.md)

### External
- 📖 [MDN — Events](https://developer.mozilla.org/en-US/docs/Web/Events)
- 📖 [MDN — Using Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- 📖 [javascript.info — Promises, async/await](https://javascript.info/async)
- 📖 [Loupe — Event loop visualizer](http://latentflip.com/loupe/)
- 📖 [Promisees — visualizer](https://bevacqua.github.io/promisees/)

---

> 🎯 *Sau bài này JS bạn interactive đầy đủ. Bài cuối cluster dạy **fetch API + ES modules** — gọi FastAPI backend + code modular.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 addEventListener Cơ bản + vs onclick cũ + Remove listener + Options + AbortController. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `javascript-dom/` lesson 4/5. Cover: addEventListener + 20+ event types (click/input/submit/keyboard/mouse/touch) + event bubbling + delegation + preventDefault + stopPropagation + Promise + async/await + setTimeout/setInterval + microtask vs task queue.
