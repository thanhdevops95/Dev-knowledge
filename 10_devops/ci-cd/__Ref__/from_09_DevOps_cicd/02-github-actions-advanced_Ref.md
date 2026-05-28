# 🤖 GitHub Actions nâng cao — Tự động hóa CI/CD

> `[INTERMEDIATE]` — Biến GitHub thành Server Automation

---

## 1. Cấu trúc một Workflow chuẩn

Một workflow file đặt tại `.github/workflows/main.yml`.

```yaml
name: Production CI/CD

# 1. KHI NÀO CHẠY? (Events)
on:
  push:
    branches: [ "main", "master" ]
  pull_request:                    # Mọi PR mở ra đều phải chạy
    branches: [ "main" ]
  schedule:                        # Chạy định kỳ giống Cronjob
    - cron: '0 2 * * *'            # (2h sáng mỗi ngày)
  workflow_dispatch:               # Cho phép bấm nút chạy tay trên Web

# 2. CHẠY CÁI GÌ? (Jobs)
jobs:
  # Job 1: Build và Test song song nhiều bản Node
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:  # Chạy job này 3 lần cho 3 ver Node khác nhau!
        node-version: [16.x, 18.x, 20.x]

    steps:
    # Lấy code về
    - name: Checkout Repository
      uses: actions/checkout@v4

    # Cài Node.js
    - name: Setup Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'  # KÍCH HOẠT CACHE NPM TỰ ĐỘNG! Tốc độ x3.

    - name: Install dependencies
      run: npm ci     # Dùng 'ci' thay 'install' để tốc độ cài siêu nhanh, bám sát lockfile

    - name: Run Linter & Tests
      run: |
        npm run lint
        npm test

  # Job 2: Đẩy ảnh Docker (Chỉ chạy khi Job test phía trên THÀNH CÔNG)
  build_docker:
    needs: test       # 👈 Phụ thuộc nè!
    if: github.event_name == 'push'  # Không build ảnh nếu chỉ là Pull Request chưa Merge.
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Đăng nhập vào Github Container Registry (ghcr.io)
      - name: Log in to the Container registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}          # Biến có sẵn của Github
          password: ${{ secrets.GITHUB_TOKEN }}  # Token động, bảo mật tuyệt đối

      # Build và Push!
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          pwd: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

---

## 2. Secrets Management (Bảo mật thông tin nhảy cảm)

Tuyệt đối không để Token, Password mộc cởi truồng lộ thiên trong `.yml`. Sẽ bị bots quét và hack trong 5 phút.

**Cách làm:**
1. Vào Repo Github -> Settings -> Secrets and variables -> Actions.
2. Thêm Secret: `AWS_ACCESS_KEY_ID = ABCXYZ123`.
3. Gọi nó ra xài an toàn:

```yaml
- name: Deploy to AWS
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }} # Màn hình Actions sẽ thay chỗ này bằng dấu "***"
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: aws s3 sync ./dist s3://my-bucket
```

---

## 3. Caching Dependency (Xử lý vấn đề CI chạy quá lâu)

Cài `node_modules` hay `.m2` (Java) tốn 3 phút rưỡi. Mọi workflow chạy mất 5 phút = Tổn thất nặng nề.

```yaml
# Caching xịn xò với actions/cache
- name: Cache Node Modules
  uses: actions/cache@v3
  with:
    path: ~/.npm  # Thư mục mún gói mang đem giấu (để bữa sau lục xài lại)
    # Khóa của gói đồ = mã hash của file khóa. File chưa đổi thì Khóa chép y đúc bữa truớc -> HIT Dính phóc!
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

Nếu chạy Node/Python/Java đời mới thì các Action cài đặt mặc định (`setup-node`, `setup-python`) ĐÃ CÓ SET TINH CHỈNH SẴN việc gọi cái này. Chỉ bật `cache: 'npm'` lên là xong (Như ví dụ số 1).

---

## 4. Re-usable Workflows (Trọng dụng Code)

Nếu 10 repos (Microservices) giống y xì đúc luồng Build & Push. Copy paste 10 file yml sửa mười chỗ lặp đi chùng lại sẽ sai hoài.

**Tạo 1 repo tên `central-workflows` thả thư mục `.github/workflows/build-push.yml`:**
```yaml
# central-workflows/.github/workflows/build-push.yml
on:
  workflow_call:    # 👈 Báo cho GH biết đây là template đợi ai đó gọi tui.
    inputs:
      image_name:
        required: true
        type: string
```

**Ở 1 repo code bình thường `My-App` gõ xài:**
```yaml
jobs:
  call-workflow:
    uses: MyOrganization/central-workflows/.github/workflows/build-push.yml@main
    with:
      image_name: my-app-image
```

---

## Các lỗi thường gặp

```
❌ Sai: Viết Bash scipt dài 50 dòng trong block `run:` của yml. Lỗi 1 dấu phẩy không debug được.
✅ Đúng: Quăng đống Bash lằng nhằng đó vô 1 file shell `scripts/deploy.sh`. Rồi Github gọi `- run: bash ./scripts/deploy.sh`.

❌ Sai: Checkout source lúc push rồi mang đi Deploy luôn.
✅ Đúng: Build source trên Github Runner. Chép khối zip/tar đi Server deploy (Artifacts Passing). Server hổng có cài đồ lung tung để Build.
```

---

## Bài tập thực hành

- [ ] Tạo file action kiểm tra: Cứ ai hễ Push lên nhánh `main` là Action tự In ra chữ "Xin chào `${{ github.actor }}` đã push code!".
- [ ] Tham khảo Marketplace Github để xài 1 cái Action `ftp-deploy` đẩy thư mục ảnh html thô sơ vừa ZIP xong quăng lên 1 Host cpanel rẻ tiền nào đó.
- [ ] Thử tính huống Cố nhồi file Secret nhạy cảm vào code sau đó viết Linter chặn lại cho rớt bài Build Push ngay lập tức.
