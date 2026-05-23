# 🤖 Prompt Engineering — Viết prompt hiệu quả cho AI

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Kỹ năng tối quan trọng thời đại AI

---

## Tại sao Prompt Engineering quan trọng?

LLMs (GPT, Claude, Gemini) không đọc ý nghĩ — chúng **phản hồi dựa trên cách bạn hỏi**. Cùng 1 bài toán, prompt khác nhau cho kết quả chênh nhau **10-100x** về chất lượng.

Không phải AI dốt — mà bạn **chưa biết cách hỏi**.

```
❌ Prompt vague:
  "Giúp tôi viết code"
  → AI đoán mò, trả lời chung chung

✅ Prompt rõ ràng:
  "Viết TypeScript function validating email sử dụng regex.
   Input: string, Output: boolean.
   Handle edge cases: empty string, missing @, missing domain.
   Include JSDoc comments và unit tests với Jest."
  → AI trả code chính xác, đầy đủ test
```

**Mindset quan trọng:** Bạn đang **giao việc cho junior developer rất giỏi nhưng không biết context** — phải nói rõ:
1. Bạn muốn gì (What)
2. Ngữ cảnh nào (Context)
3. Output format nào (Format)
4. Ràng buộc gì (Constraints)

---

## 1. Cấu trúc prompt hiệu quả

### Framework: Role + Context + Task + Format

```
[ROLE] Bạn là {vai trò} với {kinh nghiệm/chuyên môn}.
[CONTEXT] Tôi đang {tình huống}. Dự án sử dụng {tech stack}.
[TASK] Hãy {hành động cụ thể}.
[FORMAT] Trả lời theo format {định dạng}. 
[CONSTRAINTS] Lưu ý: {ràng buộc, edge cases}.
```

**Ví dụ thực tế:**

```
Bạn là senior backend developer chuyên Node.js và PostgreSQL.

Tôi đang xây e-commerce API. Tech stack: NestJS, Prisma, PostgreSQL.

Hãy thiết kế database schema cho hệ thống đơn hàng bao gồm:
- Orders (id, userId, status, total, timestamps)
- OrderItems (id, orderId, productId, quantity, price)
- Status transitions: pending → confirmed → shipped → delivered

Trả lời bao gồm:
1. Prisma schema
2. Migration SQL
3. Indexes cần thiết và lý do

Lưu ý:
- Hỗ trợ soft delete
- Order total phải consistent với sum of items
- Cần audit trail cho status changes
```

---

## 2. Techniques nâng cao

### Few-shot Learning — Cho ví dụ

AI học tốt nhất qua ví dụ. Thay vì giải thích dài dòng, cho 2-3 ví dụ:

```
Chuyển ERROR log message sang structured format:

Input: "2026-03-04 15:30:00 ERROR UserService - Failed to create user: duplicate email"
Output: {"timestamp": "2026-03-04T15:30:00Z", "level": "error", "service": "UserService", "action": "create_user", "error": "duplicate_email"}

Input: "2026-03-04 15:31:00 WARN PaymentService - Retry attempt 3/5 for order #123"
Output: {"timestamp": "2026-03-04T15:31:00Z", "level": "warn", "service": "PaymentService", "action": "payment_retry", "details": {"attempt": 3, "max": 5, "orderId": "123"}}

Input: "2026-03-04 15:32:00 ERROR DatabaseService - Connection pool exhausted, 50 active connections"
Output:
```

AI sẽ tự suy ra pattern và trả đúng format.

### Chain-of-Thought — Bắt AI suy nghĩ từng bước

```
Phân tích security của đoạn code sau. Suy nghĩ từng bước:

1. Đầu tiên, liệt kê tất cả input points (user-controlled data)
2. Với mỗi input, trace data flow qua code
3. Kiểm tra có sanitization/validation không
4. Nếu thiếu → xác định vulnerability type (XSS, SQLi, etc.)
5. Đề xuất fix cụ thể

Code:
```javascript
app.get('/search', (req, res) => {
    const q = req.query.q;
    const result = db.query(`SELECT * FROM products WHERE name LIKE '%${q}%'`);
    res.send(`<h1>Results for: ${q}</h1>`);
});
```

→ AI sẽ phân tích kỹ hơn nhiều so với chỉ hỏi "code này có lỗi gì?"

### System Prompt — Định hình behavior

```
System prompt (cho chatbot/API):

Bạn là assistant phân tích code. Rules:
1. Luôn chỉ ra cả ĐÚNG và SAI trong code
2. Mọi suggestion phải kèm LÝ DO
3. Nếu có nhiều cách fix, liệt kê trade-offs
4. Respond bằng tiếng Việt, code comments bằng English
5. Không bao giờ suggest deprecated APIs
6. Format: dùng markdown, code blocks có syntax highlighting
```

---

## 3. Anti-patterns — Những cách hỏi tệ

### ❌ Quá mơ hồ

```
❌ "Giúp tôi với code"
✅ "Fix null pointer exception ở line 15 trong function `processOrder`. 
    Error: Cannot read property 'id' of undefined.
    Input data có thể missing 'customer' field."
```

### ❌ Quá nhiều trong 1 prompt

```
❌ "Thiết kế database, viết API, tạo UI, deploy lên AWS cho app chat"

✅ Chia nhỏ:
   Prompt 1: "Thiết kế database schema cho chat app: users, conversations, messages"
   Prompt 2: "Dựa trên schema trên, viết REST API với NestJS"
   Prompt 3: "Viết React components cho chat interface"
```

### ❌ Không cho context

```
❌ "Tại sao code này không chạy?"
✅ "Code: [paste code]
    Error message: [paste error]
    Runtime: Node.js 20, TypeScript 5.3
    Tôi expect: function return array of users
    Thực tế: return undefined"
```

---

## 4. Prompt cho từng use case

### Code Review

```
Review code sau với vai trò senior engineer. Focus vào:
1. Bug tiềm ẩn (null checks, edge cases, race conditions)
2. Performance (N+1 queries, unnecessary re-renders)
3. Security (injection, XSS, data exposure)
4. Readability (naming, structure, comments)

Severity levels: 🔴 Critical | 🟡 Warning | 🟢 Suggestion
```

### Debug Assistance

```
Tôi gặp bug: [mô tả behavior]
Expected: [expected behavior]
Actual: [actual behavior]
Error log: [paste error]

Đã thử:
1. [điều đã thử]
2. [điều đã thử]

Tech stack: [list]
Code: [paste relevant code]
```

### Architecture Design

```
Context: Tôi đang thiết kế [hệ thống gì] cho [bao nhiêu users].

Requirements:
- [Functional requirement 1]
- [Functional requirement 2]

Constraints:
- Budget: [...]
- Team: [size, experience]
- Timeline: [...]

Hãy đề xuất architecture bao gồm:
1. High-level diagram (text-based)
2. Tech stack với lý do chọn
3. Trade-offs và risks
4. Scaling strategy
```

---

## 5. Tips tổng hợp

| # | Tip | Tại sao |
|---|---|---|
| 1 | Cụ thể hơn → tốt hơn | AI không đoán ý bạn được |
| 2 | Cho ví dụ input/output | AI hiểu format bạn muốn |
| 3 | Yêu cầu "think step by step" | Giảm lỗi logic |
| 4 | Nói "explain your reasoning" | Kiểm chứng logic của AI |
| 5 | Iterate! Prompt 1 → feedback → prompt 2 | Refinement > one-shot |
| 6 | Assign role cụ thể | AI adjust expertise level |
| 7 | Set constraints rõ ràng | Tránh output quá rộng |
| 8 | Chia task lớn thành nhỏ | Mỗi prompt = 1 task focused |

---

## Bài tập thực hành

- [ ] Viết prompt cho AI review code: so sánh kết quả giữa prompt vague vs structured
- [ ] Few-shot: cho 3 ví dụ log parsing, test với log mới
- [ ] Chain-of-thought: debug 1 bug phức tạp step-by-step
- [ ] System prompt: tạo chatbot hỗ trợ kỹ thuật cho sản phẩm của bạn

---

## Tài nguyên thêm

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Learn Prompting](https://learnprompting.org/) — Free course
