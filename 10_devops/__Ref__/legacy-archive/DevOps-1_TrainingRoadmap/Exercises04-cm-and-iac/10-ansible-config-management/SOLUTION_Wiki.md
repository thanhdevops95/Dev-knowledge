# Lời giải và Hướng dẫn - Bài 10: Ansible

Chào mừng bạn đến với bài thực hành Ansible. Tôi đã chuẩn bị các file cấu hình cần thiết để bạn có thể chạy một playbook hoàn chỉnh trên chính máy tính của mình.

**Yêu cầu:**
-   Máy tính của bạn đã được cài đặt Ansible.
-   Bạn có quyền `sudo` trên máy.

**⚠️ Cảnh báo Quan trọng:** Playbook này sẽ sử dụng quyền `sudo` để **cài đặt phần mềm Nginx** lên máy tính của bạn.

---

### Giải thích các file đã tạo

Trong thư mục này, bạn sẽ thấy:
-   `hosts`: File inventory, định nghĩa các máy chủ mà Ansible sẽ quản lý. Trong trường hợp này, nó chỉ định `localhost` (chính máy tính của bạn).
-   `index.html`: Một file HTML đơn giản để chúng ta sao chép lên web server.
-   `playbook.yml`: File "kịch bản" chứa các chỉ dẫn để cài đặt và cấu hình Nginx. Đây là phiên bản cuối cùng đã áp dụng các khái niệm từ cả 4 bài tập.

---

### Bài 1: Cấu hình Inventory và Chạy Ad-hoc command

**Mục tiêu:** Xác nhận Ansible đã được cài đặt và có thể kết nối đến máy chủ trong inventory.

1.  **Phân tích file `hosts`:**
    Nội dung file `hosts` của chúng ta là:
    ```ini
    [local]
    localhost ansible_connection=local
    ```
    -   `[local]`: Định nghĩa một nhóm máy chủ tên là `local`.
    -   `localhost ansible_connection=local`: Khai báo rằng máy chủ `localhost` thuộc nhóm này và Ansible nên chạy các lệnh trực tiếp trên máy thay vì kết nối qua SSH.

2.  **Chạy Ad-hoc command:**
    Mở terminal trong thư mục này và chạy lệnh sau:
    ```bash
    ansible all -i hosts -m ping
    ```
    -   **Giải thích:**
        -   `ansible all`: Chạy một lệnh ad-hoc trên `all` (tất cả) các máy chủ.
        -   `-i hosts`: Sử dụng file `hosts` làm inventory.
        -   `-m ping`: Sử dụng module `ping` của Ansible. Đây không phải là lệnh ping ICMP thông thường, mà là một module kiểm tra xem Ansible có thể kết nối và thực thi Python trên máy đích hay không.

    -   **Kết quả mong đợi:** Bạn sẽ thấy một khối output màu xanh lá cây, cho thấy kết nối đã thành công.
        ```json
        localhost | SUCCESS => {
            "changed": false,
            "ping": "pong"
        }
        ```

---

### Bài 2: Viết và Chạy Playbook cài đặt Nginx

**Mục tiêu:** Thực thi một playbook để tự động hóa việc cài đặt và cấu hình một dịch vụ.

1.  **Chạy playbook:**
    ```bash
    ansible-playbook -i hosts playbook.yml -K
    ```
    -   **Giải thích:**
        -   `ansible-playbook`: Lệnh để chạy một file playbook YAML.
        -   `-K` (viết hoa): Yêu cầu Ansible hỏi mật khẩu `sudo` (`become_pass`) của bạn khi cần thiết để thực thi các tác vụ yêu cầu quyền cao.

2.  **Quan sát Output:**
    Lần đầu tiên chạy, bạn sẽ thấy các tác vụ có màu **vàng (changed)**, báo hiệu rằng Ansible đã thực hiện một thay đổi trên hệ thống (ví dụ: đã cài đặt Nginx, đã copy file).

3.  **Kiểm tra kết quả:**
    Mở trình duyệt và truy cập `http://localhost`. Bạn sẽ thấy trang web với nội dung "Hello from Ansible!".

---

### Bài 3: Trải nghiệm tính Idempotency

**Mục tiêu:** Hiểu được một trong những tính năng mạnh mẽ nhất của Ansible.

1.  **Chạy lại playbook:**
    Không thay đổi bất kỳ file nào, hãy chạy lại chính xác lệnh trên:
    ```bash
    ansible-playbook -i hosts playbook.yml -K
    ```

2.  **Quan sát Output:**
    Lần này, các tác vụ sẽ có màu **xanh lá cây (ok)**. Ở phần tóm tắt `PLAY RECAP` cuối cùng, bạn sẽ thấy `changed=0`.

    -   **Giải thích:** Đây chính là **tính idempotent**. Ansible đã kiểm tra hệ thống:
        -   Nó thấy package `nginx` đã được cài đặt -> `ok`.
        -   Nó thấy file `/var/www/html/index.html` đã có nội dung chính xác -> `ok`.
        -   Vì không có gì thay đổi, handler "Restart Nginx" không được gọi.

    Ansible chỉ thay đổi hệ thống khi cần thiết để đạt được trạng thái mong muốn bạn đã định nghĩa.

---

### Bài 4: Sử dụng Biến (Variables)

**Mục tiêu:** Làm cho playbook trở nên linh hoạt và dễ bảo trì hơn.

1.  **Phân tích `playbook.yml`:**
    Hãy nhìn vào file `playbook.yml` đã được cung cấp. Bạn sẽ thấy một khối `vars` ở đầu:
    ```yaml
    vars:
      package_name: nginx
      service_name: nginx
    ```
    Và trong các task, thay vì viết cứng `nginx`, chúng ta sử dụng cú pháp `{{ ... }}` để tham chiếu đến các biến này:
    ```yaml
    - name: Install {{ package_name }}
      apt:
        name: "{{ package_name }}"
    ```

2.  **Lợi ích:**
    Giả sử bạn muốn chạy playbook này trên một hệ điều hành khác như CentOS, nơi web server có tên là `httpd`. Thay vì phải tìm và sửa tất cả những nơi có chữ `nginx` trong playbook, bạn chỉ cần thay đổi giá trị của các biến ở một nơi duy nhất:
    ```yaml
    vars:
      package_name: httpd
      service_name: httpd
    ```
    Điều này làm cho playbook của bạn dễ dàng tái sử dụng và bảo trì hơn rất nhiều.

Chúc mừng bạn đã hoàn thành bài thực hành về Ansible!