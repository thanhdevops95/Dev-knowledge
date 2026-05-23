# Bài 10: Ansible - Quản lý Cấu hình

## 🎯 Mục tiêu bài học

-   Hiểu được khái niệm Quản lý cấu hình (Configuration Management) và tại sao nó quan trọng.
-   Nắm được kiến trúc của Ansible (Control Node, Managed Nodes, agentless).
-   Viết được một Inventory để định nghĩa danh sách các máy chủ cần quản lý.
-   Viết được một Playbook đơn giản để tự động hóa một tác vụ (ví dụ: cài đặt Nginx).
-   Hiểu và sử dụng được các khái niệm cốt lõi: `Playbook`, `Task`, `Module`, `Handler`.

## 📖 Nội dung chính

1.  **Quản lý cấu hình là gì?** Vấn đề của việc cấu hình thủ công.
2.  **Giới thiệu Ansible:** Đơn giản, không cần agent (agentless), và mạnh mẽ.
3.  **Kiến trúc Ansible:** Control Node và Managed Nodes.
4.  **Inventory:** "Danh bạ" các máy chủ của bạn.
5.  **Ad-Hoc Commands:** Chạy các lệnh nhanh trên nhiều máy chủ.
6.  **Playbooks:** Trái tim của Ansible, định nghĩa các tác vụ tự động hóa.
    -   `hosts`: Chạy trên máy chủ nào?
    -   `tasks`: Cần làm những gì?
    -   `modules`: Các "viên gạch" để xây dựng task (ví dụ: `apt`, `copy`, `service`).
    -   `handlers`: Các task đặc biệt chỉ chạy khi có thông báo.
7.  **Thực hành:** Viết playbook cài đặt và khởi động web server Nginx.

## 🛠️ Công cụ & Lý thuyết

-   **Công cụ CM:** <u>Ansible</u>, Puppet, Chef, SaltStack.
-   **Công cụ dòng lệnh:** `ansible`, `ansible-playbook`.
-   **Lý thuyết:** Configuration Management, Push vs. Pull model, Idempotency, YAML.

---

# Nội dung chi tiết - Bài 10: Ansible - Quản lý Cấu hình

Sau khi đã có thể đóng gói ứng dụng bằng Docker và điều phối chúng bằng Kubernetes, chúng ta cần một cách để chuẩn bị và cấu hình các máy chủ (server) sẽ chạy những container đó. Việc cài đặt phần mềm, cấu hình file, quản lý dịch vụ... trên hàng chục, hàng trăm máy chủ bằng tay là điều không thể. Đây là lúc công cụ Quản lý Cấu hình (Configuration Management - CM) như Ansible tỏa sáng.

---

### 1. Quản lý cấu hình là gì?

Quản lý Cấu hình là quá trình tự động hóa việc cài đặt, cấu hình và quản lý các máy chủ để đảm bảo chúng luôn ở một trạng thái nhất quán và định trước.

**Vấn đề:**
-   **Configuration Drift:** Theo thời gian, cấu hình của các máy chủ trong cùng một cụm có thể trở nên khác biệt do các thay đổi thủ công, gây ra các lỗi khó lường.
-   **Khó khăn khi mở rộng:** Khi cần thêm 10 máy chủ mới, bạn phải lặp lại toàn bộ quá trình cấu hình một cách thủ công.
-   **Không có tài liệu:** Trạng thái của máy chủ chỉ tồn tại trên chính nó, không được ghi lại dưới dạng code.

Ansible giải quyết những vấn đề này bằng cách cho phép bạn định nghĩa trạng thái mong muốn của máy chủ trong các file văn bản (code).

---

### 2. Giới thiệu Ansible

Ansible là một công cụ CM cực kỳ phổ biến vì các đặc tính sau:
-   **Đơn giản:** Sử dụng cú pháp YAML rất dễ đọc, dễ viết.
-   **Không cần Agent (Agentless):** Ansible không yêu cầu cài đặt bất kỳ phần mềm (agent) nào lên các máy chủ cần quản lý (Managed Node). Nó giao tiếp với các máy chủ này thông qua SSH (đối với Linux) hoặc WinRM (đối với Windows). Điều này làm cho việc triển khai và sử dụng Ansible trở nên vô cùng đơn giản.
-   **Mạnh mẽ:** Có hàng ngàn module được xây dựng sẵn cho hầu hết mọi tác vụ, từ quản lý package, user, service cho đến tương tác với các dịch vụ đám mây.

---

### 3. Kiến trúc Ansible

-   **Control Node:** Là máy tính mà bạn cài đặt Ansible và từ đó bạn chạy các lệnh `ansible` hoặc `ansible-playbook`.
-   **Managed Nodes:** Là các máy chủ mà Ansible quản lý. Chúng được định nghĩa trong file inventory.

---

### 4. Inventory

Inventory là một file (thường là INI hoặc YAML) định nghĩa danh sách các máy chủ mà Ansible có thể kết nối và quản lý.

*Ví dụ: file `hosts` (dạng INI)*
```ini
[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11

[databases]
db1.example.com
```
File này định nghĩa 2 nhóm máy chủ: `webservers` và `databases`.

---

### 5. Ad-Hoc Commands

Đây là cách để chạy nhanh một lệnh Ansible mà không cần viết playbook. Rất hữu ích cho các tác vụ đơn giản.

```bash
# Ping tất cả các máy chủ trong inventory
ansible all -m ping

# Kiểm tra dung lượng ổ đĩa trên nhóm webservers
ansible webservers -m command -a "df -h"
```
-   `-m`: Chỉ định module cần sử dụng.
-   `-a`: Các tham số cho module.

---

### 6. Playbooks

Playbook là trái tim của Ansible. Nó là một file YAML định nghĩa một tập hợp các tác vụ (tasks) sẽ được thực thi trên một nhóm máy chủ.

**Các khái niệm chính:**

-   **`play`**: Một playbook có thể chứa nhiều `play`. Mỗi `play` là một mapping giữa một nhóm máy chủ và các tác vụ.
-   **`hosts`**: Chỉ định `play` này sẽ chạy trên nhóm máy chủ nào trong inventory.
-   **`tasks`**: Một danh sách các tác vụ cần thực hiện. Ansible sẽ thực thi chúng tuần tự.
-   **`module`**: Mỗi task sẽ gọi một module. Module là đơn vị thực thi công việc thực tế. Ví dụ: `apt` module để quản lý package trên Ubuntu/Debian, `service` module để quản lý dịch vụ.
-   **`handler`**: Là một task đặc biệt chỉ được kích hoạt (triggered) bởi một task khác. Công dụng phổ biến nhất là khởi động lại một dịch vụ chỉ khi file cấu hình của nó thay đổi.

---

### 7. Thực hành: Playbook cài đặt Nginx

*File `install_nginx.yml`:*
```yaml
---
- hosts: webservers
  become: yes # Chạy các task với quyền sudo (root)
  tasks:
    - name: Install Nginx # Tên của task, sẽ được in ra khi chạy
      apt:
        name: nginx
        state: present # Đảm bảo package nginx đã được cài đặt
      notify: # Gửi thông báo đến handler
        - Restart Nginx

    - name: Copy custom index page
      copy:
        src: ./index.html # File trên Control Node
        dest: /var/www/html/index.html # Đường dẫn trên Managed Node
      notify:
        - Restart Nginx

  handlers:
    - name: Restart Nginx
      service:
        name: nginx
        state: restarted # Chỉ khởi động lại nếu có thông báo
```
**Chạy playbook:**
```bash
ansible-playbook -i hosts install_nginx.yml
```
**Tính Idempotency:** Một đặc tính quan trọng của Ansible là **idempotency**. Nếu bạn chạy playbook này 100 lần, Nginx sẽ chỉ được cài đặt ở lần đầu tiên. Những lần sau, Ansible sẽ kiểm tra và thấy Nginx đã được cài rồi, và nó sẽ không làm gì cả. Điều này đảm bảo hệ thống luôn ở đúng trạng thái bạn mong muốn mà không gây ra các thay đổi không cần thiết.

## ✍️ Bài tập thực hành (Exercises)

Phần này sẽ hướng dẫn bạn chạy playbook Ansible đầu tiên trên chính máy tính của mình.

**Yêu cầu:**
-   Cài đặt Ansible trên máy của bạn (Control Node). Tham khảo [hướng dẫn cài đặt Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).
-   Nếu bạn dùng Linux/macOS, bạn đã có sẵn SSH.
-   Bạn cần có quyền `sudo` trên máy.

**Bài 1: Cấu hình Inventory và Chạy Ad-hoc command**
1.  Tạo một thư mục mới cho bài thực hành, ví dụ `ansible-practice`.
2.  Bên trong thư mục đó, tạo một file inventory tên là `hosts`.
3.  Để Ansible chạy trên chính máy local của bạn, thêm nội dung sau vào file `hosts`:
    ```ini
    [local]
    localhost ansible_connection=local
    ```
    *Ghi chú: `ansible_connection=local` báo cho Ansible biết không cần dùng SSH mà hãy chạy lệnh trực tiếp trên máy Control Node.*
4.  Mở terminal trong thư mục `ansible-practice` và kiểm tra kết nối bằng một ad-hoc command:
    ```bash
    ansible all -i hosts -m ping
    ```
    Bạn sẽ thấy output màu xanh với ` "ping": "pong" ` và `"changed": false,`.
5.  Thử một lệnh khác để lấy thông tin hệ điều hành: `ansible all -i hosts -m setup | grep ansible_os_family`.

**Bài 2: Viết và Chạy Playbook cài đặt Nginx**
1.  Trong cùng thư mục `ansible-practice`, tạo một file `index.html` đơn giản với nội dung: `<h1>Hello from Ansible!</h1>`.
2.  Tạo file playbook `install_nginx.yml`. Sao chép nội dung từ phần hướng dẫn số 7, nhưng **thay đổi một dòng quan trọng**:
    -   Thay `hosts: webservers` thành `hosts: local`.
3.  Chạy playbook của bạn. Lệnh `-K` sẽ hỏi bạn mật khẩu `sudo` khi cần.
    ```bash
    ansible-playbook -i hosts install_nginx.yml -K
    ```
4.  Sau khi playbook chạy xong, mở trình duyệt và truy cập `http://localhost`. Bạn có thấy trang "Hello from Ansible!" không? (Nếu bạn dùng macOS, Nginx có thể chạy trên port 8080).

**Bài 3: Trải nghiệm tính Idempotency**
1.  Không thay đổi gì cả, hãy chạy lại playbook một lần nữa: `ansible-playbook -i hosts install_nginx.yml -K`.
2.  Quan sát output trên terminal. Chú ý đến màu sắc và các dòng tóm tắt `PLAY RECAP`. Các task sẽ có trạng thái `ok` (màu xanh lá) thay vì `changed` (màu vàng) như lần đầu.
3.  Điều này chứng tỏ **tính idempotent** của Ansible: nó đã kiểm tra và thấy Nginx đã được cài, file `index.html` đã đúng nội dung, nên nó không thực hiện lại các hành động đó nữa.

**Bài 4: Sử dụng Biến (Variables)**
1.  Sửa file `install_nginx.yml` để làm cho nó linh hoạt hơn bằng cách sử dụng biến.
2.  Ở đầu playbook (cùng cấp với `hosts`, `become`), thêm khối `vars`:
    ```yaml
    vars:
      package_name: nginx
      service_name: nginx
    ```
3.  Trong task `Install Nginx`, thay `name: nginx` thành `name: "{{ package_name }}"`.
4.  Trong handler `Restart Nginx`, thay `name: nginx` thành `name: "{{ service_name }}"`.
5.  Chạy lại playbook để xác nhận nó vẫn hoạt động bình thường. Việc này giúp bạn dễ dàng thay đổi tên package (ví dụ `httpd` trên CentOS) ở một nơi duy nhất.

---

Trong bài học tiếp theo, chúng ta sẽ tiến một bước xa hơn trong việc quản lý hạ tầng bằng code với Terraform.

[Bài trước: Kubernetes (K8s) - Điều phối Container](../09-kubernetes-basics/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Terraform - Hạ tầng dưới dạng Mã](../11-terraform-iac/)