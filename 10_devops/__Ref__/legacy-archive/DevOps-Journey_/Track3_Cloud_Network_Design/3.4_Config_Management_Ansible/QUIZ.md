# ❓ Quiz: Ansible

> **Knowledge Check for Configuration Management with Ansible (5 Questions)**
>
> *Kiểm tra kiến thức quản lý cấu hình với Ansible (5 câu hỏi).*

---

### Q1: Connection Protocol

What protocol does Ansible use to connect?

*(Ansible sử dụng protocol gì để connect?)*

- a) HTTP
- b) SSH
- c) RDP
- d) Telnet

---

### Q2: Agentless Meaning

What does "Ansible is agentless" mean?

*(Ansible là agentless có nghĩa gì?)*

- a) No agent needed on target *(Không cần agent trên target)*
- b) No API *(Không có API)*
- c) No UI *(Không có UI)*
- d) No config *(Không có config)*

---

### Q3: Playbook Format

What format are Ansible Playbooks written in?

*(Ansible Playbook viết bằng?)*

- a) JSON
- b) XML
- c) YAML
- d) INI

---

### Q4: Become Directive

What does `become: yes` do?

*(`become: yes` dùng để?)*

- a) Change user *(Đổi người dùng)*
- b) Run as root *(Chạy dưới quyền root)*
- c) Change host
- d) Debug

---

### Q5: Handler Execution

When does a Handler run?

*(Handler chạy khi nào?)*

- a) Always *(Luôn luôn)*
- b) When notified *(Khi được thông báo)*
- c) Before tasks *(Trước các task)*
- d) Never *(Không bao giờ)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | b | SSH for Linux, WinRM for Windows |
| 2 | a | No software needed on managed nodes |
| 3 | c | YAML-based playbooks |
| 4 | b | Escalate to root/sudo |
| 5 | b | Only when notified by a task |

</details>

---

**[← Back to README](./README.md)**
