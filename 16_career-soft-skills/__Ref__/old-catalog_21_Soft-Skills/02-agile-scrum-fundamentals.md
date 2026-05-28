# 🏃 Agile & Scrum — Quy trình phát triển phần mềm

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Cách hầu hết team phần mềm làm việc

---

## Tại sao cần Agile?

```
❌ Waterfall (truyền thống):
  Requirements → Design → Code → Test → Deploy
  (6-12 tháng) → Cuối mới biết có đúng yêu cầu không! 💀

✅ Agile:
  Sprint 1 (2 tuần): Requirements → Code → Test → Deploy → Feedback
  Sprint 2 (2 tuần): Adjustments → Code → Test → Deploy → Feedback
  Sprint 3 (2 tuần): New features → Code → Test → Deploy → Feedback
  → Feedback LIÊN TỤC, adjust NHANH
```

---

## 1. Agile Manifesto — 4 giá trị cốt lõi

```
Individuals & interactions    >  Processes & tools
Working software              >  Comprehensive documentation
Customer collaboration        >  Contract negotiation
Responding to change          >  Following a plan

→ Vế trái quan trọng HƠN, nhưng vế phải vẫn CÓ giá trị
```

---

## 2. Scrum Framework

```
Product Backlog          Sprint Backlog         Sprint (2 tuần)
┌──────────────┐        ┌──────────────┐       ┌────────────────┐
│ User Story 1 │  ───►  │ Task 1.1     │  ───► │ Daily Standup  │
│ User Story 2 │  ───►  │ Task 1.2     │       │ (mỗi ngày 15') │
│ User Story 3 │        │ Task 2.1     │       │                │
│ User Story 4 │        │ Task 2.2     │       │ Code → Test    │
│ User Story 5 │        └──────────────┘       │ → Review       │
│ ...          │         Sprint Planning        │ → Deploy       │
└──────────────┘         (đầu sprint)          └───────┬────────┘
  Product Owner                                         │
  ưu tiên backlog                                Sprint Review
                                                 Sprint Retrospective
                                                 (cuối sprint)
```

### Các vai trò

| Vai trò | Trách nhiệm |
|---|---|
| **Product Owner** | Định hướng sản phẩm, ưu tiên backlog, đại diện khách hàng |
| **Scrum Master** | Facilitator, loại bỏ blockers, bảo vệ team |
| **Development Team** | Tự tổ chức, cross-functional, deliver working software |

### Các sự kiện (Ceremonies)

```
Sprint Planning (2-4h):
  → Team chọn items từ Product Backlog → Sprint Backlog
  → Commit: "Sprint này chúng ta hoàn thành X, Y, Z"

Daily Standup (15 phút):
  → Mỗi người trả lời 3 câu:
    1. Hôm qua làm gì?
    2. Hôm nay làm gì?
    3. Có blocker gì không?

Sprint Review (1-2h):
  → Demo sản phẩm cho stakeholders
  → Thu thập feedback

Sprint Retrospective (1h):
  → Team tự đánh giá:
    ✅ Điều gì tốt? (Keep)
    ❌ Điều gì chưa tốt? (Stop)
    💡 Cải thiện gì? (Start)
```

---

## 3. User Stories & Estimation

### Viết User Story

```
As a [loại người dùng],
I want to [hành động],
So that [mục đích/giá trị].

Ví dụ:
"As a customer,
 I want to reset my password via email,
 So that I can regain access when I forget my password."

Acceptance Criteria:
✅ User nhận email reset trong vòng 2 phút
✅ Link reset hết hạn sau 1 giờ
✅ Password mới phải >= 8 ký tự
✅ Hiển thị thông báo thành công sau khi đổi
```

### Story Points — Ước lượng

```
Fibonacci: 1, 2, 3, 5, 8, 13, 21

1 point:  Login form (đơn giản, đã làm nhiều)
2 points: Password reset
3 points: User profile page
5 points: Payment integration
8 points: Search with filters + pagination
13 points: Chat real-time
21 points: Quá lớn → chia nhỏ!

Planning Poker:
  1. PO đọc user story
  2. Mỗi dev ĐỒNG THỜI chọn số
  3. Lật bài → Thảo luận chênh lệch
  4. Vote lại → Consensus
```

---

## 4. Kanban — Alternative cho Scrum

```
Kanban Board:
┌──────────┬───────────┬───────────┬──────────┬──────────┐
│ Backlog  │ To Do     │ In Prog.  │ Review   │   Done   │
│          │ (limit:3) │ (limit:2) │(limit:2) │          │
├──────────┼───────────┼───────────┼──────────┼──────────┤
│ Story 6  │ Story 3   │ Story 2   │ Story 1  │ Story A  │
│ Story 7  │ Story 4   │ Story 5   │          │ Story B  │
│ Story 8  │           │           │          │ Story C  │
│ ...      │           │           │          │          │
└──────────┴───────────┴───────────┴──────────┴──────────┘
                         WIP Limit
```

### Scrum vs Kanban

| | Scrum | Kanban |
|---|---|---|
| **Iteration** | Sprint cố định (2 tuần) | Liên tục (continuous flow) |
| **Roles** | PO, SM, Dev Team | Không bắt buộc |
| **Planning** | Sprint Planning | Just-in-time |
| **WIP Limit** | Sprint capacity | Per column |
| **Changes** | Không đổi trong sprint | Bất cứ lúc nào |
| **Khi nào** | Team mới, cần structure | Ops, support, maintenance |

---

## 5. Definition of Done (DoD)

```
Một task/story CHƯA XONG nếu chưa:
☐ Code reviewed (ít nhất 1 reviewer approved)
☐ Unit tests viết và pass (>80% coverage)
☐ Integration tests pass
☐ Documentation cập nhật (nếu cần)
☐ Deploy lên staging thành công
☐ QA verified
☐ No known bugs
☐ Performance acceptable
```

---

## 6. Metrics — Đo lường

```
Velocity:
  Sprint 1: 20 points
  Sprint 2: 25 points
  Sprint 3: 22 points
  Average: ~22 points/sprint → Dùng để estimate sprint tiếp theo

Burndown Chart:
  Story Points
  25 │╲
  20 │  ╲──── Ideal line
  15 │    ╲
  10 │      ╲──── Actual
   5 │        ╲
   0 │──────────╲───
     Day 1  5  10  14

Lead Time:  Từ khi tạo task → task done
Cycle Time: Từ khi bắt đầu làm → task done
```

---

## 7. Agile cho Developer

```
✅ Practices hay:
• Pair Programming — 2 dev 1 máy → knowledge sharing + ít bug
• Code Review — Mỗi PR phải review → chất lượng code tốt
• TDD — Test first → code later → ít regression
• CI/CD — Deploy tự động → feedback nhanh
• Refactoring — Cải thiện code liên tục

✅ Mindset:
• "Done" > "Perfect" — Ship working software
• Fail fast, learn fast — Thử → sai → sửa → nhanh
• Collaboration > Solo heroics — Team > cá nhân
• Feedback loops — Demo thường xuyên → adjust sớm
```

---

## Các lỗi thường gặp

```
❌ Sai: "Agile = không cần plan, không cần docs"
✅ Đúng: Agile VẪN có plan + docs, nhưng vừa đủ, không quá nhiều

❌ Sai: Sprint = deadline cứng → dev vắt sức cuối sprint
✅ Đúng: Sprint scope có thể adjust. Sustainable pace > burnout

❌ Sai: "Standup = báo cáo cho manager"
✅ Đúng: Standup = sync GIỮA team members để giúp đỡ nhau
```

---

## Bài tập thực hành

- [ ] Viết 5 user stories cho 1 app (todo, blog, e-commerce)
- [ ] Estimate stories bằng Planning Poker với team
- [ ] Dùng GitHub Projects / Jira / Trello tạo Kanban board
- [ ] Chạy 1 sprint 1 tuần cho side project: planning → daily → review → retro

---

## Tài nguyên thêm

- [Scrum Guide](https://scrumguides.org/) — Official (16 trang, đọc 30')
- [Agile Manifesto](https://agilemanifesto.org/) — Nguồn gốc
- [Atlassian Agile Coach](https://www.atlassian.com/agile) — Tutorials miễn phí
