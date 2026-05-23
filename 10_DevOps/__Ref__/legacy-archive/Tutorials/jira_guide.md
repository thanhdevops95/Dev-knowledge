# Hướng dẫn Jira

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Jira là công cụ quản lý dự án và issue tracking phổ biến nhất, đặc biệt trong phát triển phần mềm Agile.

---

## 🔑**KHÁI NIỆM CƠ BẢN**

### Các loại Issue

| Loại | Icon | Mô tả |
|------|------|-------|
| **Epic** | 🟣 | Nhóm lớn các tính năng |
| **Story** | 🟢 | User story - tính năng từ góc nhìn người dùng |
| **Task** | 🔵 | Công việc cụ thể |
| **Sub-task** | ⚪ | Công việc con của Task/Story |
| **Bug** | 🔴 | Lỗi cần sửa |

### Workflow cơ bản

```
TO DO → IN PROGRESS → IN REVIEW → DONE
```

### Hierarchy

```
Epic
├── Story 1
│   ├── Sub-task 1.1
│   └── Sub-task 1.2
├── Story 2
└── Bug 1
```

---

## 📊**SCRUM BOARD**

### Sprint

| Thuật ngữ | Mô tả |
|-----------|-------|
| **Sprint** | Khoảng thời gian cố định (1-4 tuần) |
| **Sprint Backlog** | Các issues trong sprint |
| **Sprint Goal** | Mục tiêu của sprint |
| **Velocity** | Số story points hoàn thành/sprint |

### Các cột phổ biến

```
BACKLOG → TO DO → IN PROGRESS → IN REVIEW → DONE
```

### Sprint Planning

1. Chọn issues từ **Backlog** vào **Sprint**
2. Estimate bằng **Story Points** (1, 2, 3, 5, 8, 13, 21)
3. Đảm bảo tổng points phù hợp với velocity

---

## 🎯**KANBAN BOARD**

### Đặc điểm

| Scrum | Kanban |
|-------|--------|
| Sprints cố định | Continuous flow |
| Sprint planning | No planning meetings |
| Velocity | Lead time, Cycle time |
| Commitment | WIP limits |

### WIP Limits (Work In Progress)

- Giới hạn số issues trong mỗi cột
- Ví dụ: Max 3 issues trong "In Progress"
- Ngăn chặn multitasking quá mức

---

## 📝**TẠO ISSUE**

### Thông tin cần điền

| Field | Mô tả |
|-------|-------|
| **Summary** | Tiêu đề ngắn gọn |
| **Description** | Mô tả chi tiết |
| **Issue Type** | Story, Task, Bug, etc. |
| **Priority** | Highest, High, Medium, Low, Lowest |
| **Assignee** | Người thực hiện |
| **Reporter** | Người tạo |
| **Sprint** | Sprint hiện tại |
| **Story Points** | Estimate effort |
| **Labels** | Tags để phân loại |
| **Epic Link** | Thuộc Epic nào |

### Mẫu User Story

```
AS A [role]
I WANT [feature]
SO THAT [benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### Mẫu Bug Report

```
SUMMARY: [Ngắn gọn vấn đề]

STEPS TO REPRODUCE:
1. Step 1
2. Step 2
3. Step 3

EXPECTED RESULT:
[Kết quả mong đợi]

ACTUAL RESULT:
[Kết quả thực tế]

ENVIRONMENT:
- Browser: Chrome 120
- OS: Windows 11
- Version: 1.2.3

ATTACHMENTS:
[Screenshots, logs]
```

---

## 🔍**JQL (Jira Query Language)**

### Cú pháp cơ bản

```jql
field operator value
```

### Ví dụ

```jql
# Issues được assign cho tôi
assignee = currentUser()

# Issues trong sprint hiện tại
sprint in openSprints()

# Bugs chưa xong
type = Bug AND status != Done

# Issues tạo tuần này
created >= startOfWeek()

# Issues chưa estimate
"Story Points" is EMPTY

# Issues của project cụ thể
project = "MY-PROJECT" AND status = "In Progress"

# Tìm theo text
summary ~ "login" OR description ~ "authentication"

# Issues updated gần đây
updated >= -7d

# Issues sắp hết hạn
duedate <= 3d AND status != Done

# Issues theo priority
priority in (Highest, High) AND status = "To Do"

# Issues theo label
labels = "urgent" OR labels = "critical"
```

### Operators

| Operator | Mô tả |
|----------|-------|
| `=` | Bằng |
| `!=` | Không bằng |
| `>`, `<`, `>=`, `<=` | So sánh |
| `~` | Chứa text |
| `!~` | Không chứa |
| `IS EMPTY` | Không có giá trị |
| `IS NOT EMPTY` | Có giá trị |
| `IN` | Trong danh sách |
| `NOT IN` | Không trong danh sách |
| `WAS` | Từng có giá trị |
| `CHANGED` | Đã thay đổi |

### Functions

```jql
# Current user
assignee = currentUser()

# Open sprints
sprint in openSprints()

# Closed sprints
sprint in closedSprints()

# Future sprints
sprint in futureSprints()

# Date functions
created >= startOfDay()
created >= startOfWeek()
created >= startOfMonth()
created >= startOfYear()
updated >= -7d   # 7 ngày trước
updated <= 1w    # Trong 1 tuần
```

---

## 📊**REPORTS**

### Burndown Chart

- Hiển thị công việc còn lại trong sprint
- Đường lý tưởng vs đường thực tế
- Mục tiêu: Về 0 cuối sprint

### Velocity Chart

- Story points hoàn thành mỗi sprint
- Dùng để dự đoán capacity cho sprint tiếp

### Sprint Report

- Completed issues
- Issues không hoàn thành
- Issues thêm giữa sprint

### Cumulative Flow Diagram

- Hiển thị issues trong mỗi status theo thời gian
- Phát hiện bottlenecks

---

## 🔗**INTEGRATIONS**

### GitHub/GitLab

1. Cài app Jira trên GitHub/GitLab
2. Connect repositories
3. Sử dụng issue key trong commit messages:

```bash
git commit -m "MY-123: Fix login bug"
git commit -m "[MY-456] Add new feature"
```

### Slack

1. Cài Jira Cloud app trong Slack
2. Link Jira project với Slack channel
3. Nhận notifications khi có updates

### Automation Rules

1. Vào **Project Settings** → **Automation**
2. Tạo rules:

```
WHEN: Issue transitioned to Done
THEN: Add comment "Completed! 🎉"
```

```
WHEN: Issue created with label "urgent"
THEN: Add watcher (manager)
      Send Slack message
```

---

## 👥**PERMISSIONS & ROLES**

### Project Roles

| Role | Permissions |
|------|-------------|
| **Administrator** | Full access |
| **Developer** | Create, edit, transition issues |
| **Viewer** | View only |

### Permission Schemes

- Browse Projects
- Create Issues
- Edit Issues
- Delete Issues
- Assign Issues
- Transition Issues
- Comment

---

## ⌨️**KEYBOARD SHORTCUTS**

| Shortcut | Action |
|----------|--------|
| `C` | Create issue |
| `G` + `G` | Go to issue |
| `G` + `B` | Go to board |
| `J` | Next issue |
| `K` | Previous issue |
| `O` | Open issue |
| `E` | Edit issue |
| `M` | Comment |
| `A` | Assign to me |
| `I` | Assign issue |
| `.` | Quick actions |
| `/` | Search |

---

## 📋**BEST PRACTICES**

### Issue Management

- [ ] Viết summary rõ ràng, ngắn gọn
- [ ] Thêm acceptance criteria cho stories
- [ ] Estimate tất cả issues
- [ ] Link issues liên quan
- [ ] Cập nhật status đúng lúc

### Sprint Planning

- [ ] Review và groom backlog trước sprint
- [ ] Đảm bảo issues "ready" trước khi vào sprint
- [ ] Không overcommit
- [ ] Có sprint goal rõ ràng

### Daily Standups

- What did you do yesterday?
- What will you do today?
- Any blockers?

### Sprint Review & Retrospective

- Demo completed work
- Discuss what went well
- Discuss improvements
- Create action items

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
