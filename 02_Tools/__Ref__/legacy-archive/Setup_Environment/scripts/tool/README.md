# DevOps Toolkit Scripts

Thư mục này chứa một kịch bản (script) mạnh mẽ giúp bạn tự động hóa việc cài đặt, gỡ bỏ và quản lý môi trường DevOps của mình.

## Giới thiệu `devops_toolkit.sh`

Đây là một công cụ tất-cả-trong-một được thiết kế để đơn giản hóa việc quản lý các công cụ phát triển của bạn trên cả macOS và Linux (Debian/Ubuntu).

### Các tính năng chính

-   **Quản lý Công cụ:** Dễ dàng cài đặt hoặc gỡ bỏ hàng loạt công cụ DevOps phổ biến.
-   **Đa nền tảng:** Tự động phát hiện hệ điều hành (macOS hoặc Linux) và sử dụng trình quản lý gói phù hợp (`Homebrew` cho macOS, `APT` cho Linux).
-   **Tùy biến cao:** Toàn bộ danh sách công cụ được quản lý bên ngoài thông qua file `tools.conf`. Bạn có thể dễ dàng thêm, bớt, hoặc thay đổi công cụ mà không cần sửa code của script.
-   **Tạo khóa SSH:** Tích hợp tiện ích giúp tạo nhanh một khóa SSH mới cho các dịch vụ như GitHub/GitLab.
-   **Giao diện Nâng cao:** Nếu bạn đã cài đặt `gum`, script sẽ tự động sử dụng nó để hiển thị một giao diện menu đẹp và trực quan hơn.

## Hướng dẫn sử dụng

### 1. Yêu cầu
-   **macOS:** Cần cài đặt `Homebrew`.
-   **Linux:** Script hiện chỉ hỗ trợ các bản phân phối dựa trên Debian (như Ubuntu). Cần có quyền `sudo` để cài đặt/gỡ bỏ gói.
-   **Tùy chọn:** Cài đặt `gum` để có trải nghiệm giao diện tốt nhất.

### 2. Cấp quyền thực thi
Trước khi chạy lần đầu tiên, bạn cần cấp quyền thực thi cho script:
```bash
chmod +x devops_toolkit.sh
```

### 3. Chạy Script
Để khởi chạy công cụ, chỉ cần chạy lệnh sau từ terminal:
```bash
./devops_toolkit.sh
```
Bạn sẽ thấy một menu chính cho phép bạn chọn các hành động như Cài đặt, Gỡ bỏ, hoặc Tạo khóa SSH.

## Tùy chỉnh danh sách công cụ

Bạn có thể toàn quyền kiểm soát danh sách công cụ bằng cách chỉnh sửa file `tools.conf`.

### Định dạng file
Mỗi dòng trong file đại diện cho một công cụ, theo định dạng sau (phân cách bởi dấu chấm phẩy `;`):
```
DisplayName;Type;BrewName;AptName
```
-   `DisplayName`: Tên sẽ hiển thị trên menu (ví dụ: `Visual Studio Code`).
-   `Type`: Loại công cụ, có thể là `cli` (dòng lệnh) hoặc `cask` (ứng dụng GUI trên macOS).
-   `BrewName`: Tên gói trên Homebrew (ví dụ: `visual-studio-code`).
-   `AptName`: Tên gói trên APT (ví dụ: `code`). Nếu không có, hãy để trống.

### Ví dụ
```
# Dòng comment sẽ được bỏ qua
Visual Studio Code;cask;visual-studio-code;code
Git;cli;git;git
My Awesome Tool;cli;my-tool;my-tool
```