# ❓ Quiz: Jenkins

> **Knowledge Check for Jenkins Pipelines (5 Questions)**
>
> *Kiểm tra kiến thức Jenkins Pipelines (5 câu hỏi).*
>
> 💡 **Note:** GitLab CI is the primary CI/CD platform. Jenkins is taught as an enterprise alternative.
>
> *Lưu ý: GitLab CI là nền tảng CI/CD chính. Jenkins được dạy như một giải pháp thay thế cho doanh nghiệp.*

---

### Q1: Jenkins Agent

What is a Jenkins agent?

*(Jenkins agent là gì?)*

- a) User interface *(Giao diện người dùng)*
- b) Execution environment *(Môi trường thực thi)*
- c) Plugin
- d) Configuration *(Cấu hình)*

---

### Q2: Jenkinsfile Language

What language does Jenkinsfile use?

*(Jenkinsfile dùng ngôn ngữ gì?)*

- a) YAML
- b) JSON
- c) Groovy
- d) Python

---

### Q3: Agent Any

What does `agent any` mean?

*(`agent any` có nghĩa gì?)*

- a) No agent *(Không có agent)*
- b) Run on any available agent *(Chạy trên bất kỳ agent khả dụng nào)*
- c) Docker agent
- d) Kubernetes agent

---

### Q4: Post Always Block

When does `post { always { } }` run?

*(`post { always { } }` chạy khi nào?)*

- a) Only on success *(Chỉ khi thành công)*
- b) Only on failure *(Chỉ khi thất bại)*
- c) Always *(Luôn chạy)*
- d) Never *(Không bao giờ)*

---

### Q5: Git Push Trigger

How to trigger build from Git push?

*(Cách trigger build từ Git push?)*

- a) Webhook
- b) Polling
- c) Both *(Cả hai)*
- d) Manual only *(Chỉ thủ công)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | b | Agent is where jobs run |
| 2 | c | Groovy-based DSL |
| 3 | b | Runs on any available executor |
| 4 | c | Runs regardless of build result |
| 5 | c | Both webhook and polling work |

</details>

---

**[← Back to README](./README.md)**
