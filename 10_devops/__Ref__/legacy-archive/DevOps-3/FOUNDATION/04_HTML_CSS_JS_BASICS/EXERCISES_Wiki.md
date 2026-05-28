# Exercises: Module 04 - HTML/CSS/JS BASICS

> **Bài tập Frontend cơ bản cho DevOps**

**Tổng điểm:** 100 | **Thời gian:** 45 phút | **Đạt:** 70/100

---

## PHẦN A: TRẮC NGHIỆM (30 điểm)

**Câu 1:** HTML tag cho heading lớn nhất?

- A) h1 ✓
- B) h6
- C) header
- D) head

**Câu 2:** CSS selector cho class?

- A) #classname
- B) .classname ✓
- C) classname
- D) @classname

**Câu 3:** JavaScript declare constant?

- A) var
- B) let
- C) const ✓
- D) define

**Câu 4:** Link external CSS?

- A) link rel="stylesheet" ✓
- B) style src=""
- C) css href=""
- D) import url()

**Câu 5:** Event listener syntax?

- A) onEvent()
- B) addEventListener ✓
- C) listenEvent()
- D) eventHandler()

**Câu 6:** DOM select by ID?

- A) selectById()
- B) getElement()
- C) getElementById ✓
- D) queryId()

**Câu 7:** CSS center horizontally?

- A) margin: 0 auto ✓
- B) center: true
- C) align: center
- D) position: center

**Câu 8:** Arrow function syntax?

- A) function =>
- B) () => {} ✓
- C) -> function
- D) lambda()

**Câu 9:** Parse JSON response?

- A) response.text()
- B) response.data()
- C) response.json() ✓
- D) JSON.parse(response)

**Câu 10:** Debug trong browser?

- A) alert()
- B) console.log() ✓
- C) debug()
- D) print()

---

## PHẦN B: VIẾT CODE (40 điểm)

**Câu 11:** Tạo HTML page với semantic structure (10 điểm)

```html
<!DOCTYPE html>
<html>
<head><title>Page</title></head>
<body>
  <header>Header</header>
  <main>Content</main>
  <footer>Footer</footer>
</body>
</html>
```

**Câu 12:** Style với CSS flexbox (10 điểm)

```css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

**Câu 13:** JavaScript button click (10 điểm)

```javascript
document.getElementById('btn').addEventListener('click', () => {
  console.log('Clicked!');
});
```

**Câu 14:** Fetch data từ API (10 điểm)

```javascript
fetch('/api/data')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## PHẦN C: THỰC HÀNH (30 điểm)

1. Debug error trong DevTools (10 điểm)
2. Deploy static site lên NGINX (10 điểm)
3. Optimize assets cho production (10 điểm)

---

## 📊 THANG ĐIỂM

- **90-100:** Expert ⭐⭐⭐
- **80-89:** Proficient ⭐⭐
- **70-79:** Competent ⭐
- **<70:** Cần review

**Xem SOLUTIONS.md cho đáp án chi tiết!**
