# Module 10: CD (Continuous Deployment)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **CD** | - | Continuous Deployment/Delivery - Triển khai liên tục |
| **Deployment** | - | Quá trình đưa code lên môi trường |
| **Blue-Green** | - | Chiến lược 2 môi trường, switch traffic |
| **Canary** | - | Triển khai từ từ, % nhỏ traffic trước |
| **Rolling Update** | - | Cập nhật từng instance một |
| **Rollback** | - | Quay lại phiên bản trước khi lỗi |
| **Staging** | - | Môi trường test trước production |
| **Production** | - | Môi trường thực tế phục vụ users |
| **Feature Flag** | - | Bật/tắt tính năng mà không cần deploy |
| **GitOps** | - | Quản lý infra qua Git |
| **ArgoCD** | - | Tool GitOps phổ biến cho Kubernetes |

---

## 📖 CD là gì? (Định nghĩa từ gốc)

### Trước hết: CI làm gì?

Từ Module 08, bạn biết **CI (Continuous Integration)** là:

- Developer push code → Pipeline tự động chạy
- Build, test, lint → Fail thì không merge
- Output: **Artifact đã được test** (Docker image, JAR file, etc.)

**Nhưng CI dừng ở đó.** Code đã test xong, nằm trong registry. Deploy vẫn phải làm manual.

### CD tiếp nối

> **CD = Tự động đưa artifact đã test lên môi trường (staging hoặc production)**

**Có 2 loại CD (khác nhau quan trọng):**

| Loại | Định nghĩa | Workflow |
|------|-----------|----------|
| **Continuous Delivery** | Artifact luôn **sẵn sàng** deploy, nhưng cần **approve thủ công** | CI → Artifact → **Humans approve** → Deploy |
| **Continuous Deployment** | Artifact đã pass tests → **tự động deploy** lên production | CI → Artifact → **Auto Deploy** |

```
CI:                     Code → Test → Artifact
                                         ↓
Continuous Delivery:              Manual Approval → Deploy
Continuous Deployment:            Auto Deploy (no human gate)
```

**Chọn loại nào?**

| Chọn Continuous Delivery khi... | Chọn Continuous Deployment khi... |
|--------------------------------|----------------------------------|
| Regulated industries (bank, healthcare) | Fast-moving startups |
| Cần business approval | Có test coverage cao (>80%) |
| Deploy ảnh hưởng nhiều teams | Feature flags để control risk |
| Mới bắt đầu với CD | Mature engineering culture |

### Tại sao cần CD?

**Không có CD:**

```
1. Developer: "Code đã merge!" 
2. Ops: "OK, để tôi deploy thủ công..."
3. 3 ngày sau, Ops có time → Deploy
4. Bug phát hiện sau 3 ngày, khó trace
```

**Có CD:**

```
1. Developer merge code
2. CI pass → Auto deploy staging
3. 10 phút sau: Live trên staging
4. QA approve → Auto deploy production
5. 30 phút từ merge đến production
```

---

## 🎬 Câu chuyện thực tế

**Trước CD:** Deploy là "event lớn" - mỗi tháng 1 lần, cả team thức đêm, hồi hộp.

**Sau CD:** Deploy là "non-event" - mỗi ngày 10 lần, không ai để ý vì nó tự động và an toàn.

---

## 📖 CD Strategies

Khi deploy version mới, bạn có nhiều cách. Mỗi cách có trade-offs khác nhau về **risk**, **speed**, và **complexity**. Hiểu chúng giúp bạn chọn đúng cho từng tình huống.

| Strategy | Risk | Speed | Rollback | Use case |
|----------|------|-------|----------|----------|
| **Rolling Update** | Trung bình | Nhanh | Tự động | Default, hầu hết apps |
| **Blue-Green** | Thấp | Rất nhanh | Instant | Apps cần zero downtime |
| **Canary** | Rất thấp | Chậm | Instant | Apps quan trọng, cần test với real traffic |

### 1. Rolling Update

**Cách hoạt động:** Thay thế từng Pod một. Luôn có Pods đang chạy để serve traffic.

**Ưu điểm:** Đơn giản, là default của Kubernetes.
**Nhược điểm:** Trong quá trình update, có cả v1 và v2 chạy đồng thời.

```
Pods: [v1] [v1] [v1] [v1]
          ↓
      [v1] [v1] [v1] [v2]
          ↓
      [v1] [v1] [v2] [v2]
          ↓
      [v2] [v2] [v2] [v2]
```

> 💡 **Khi nào dùng:** Hầu hết các apps. Đơn giản và hiệu quả.

### 2. Blue-Green Deployment

**Cách hoạt động:** Có 2 môi trường giống hệt nhau (Blue và Green). Deploy version mới lên môi trường "Green", test xong thì switch traffic.

**Ưu điểm:** Zero downtime, rollback instant (chỉ cần switch traffic lại).
**Nhược điểm:** Cần gấp đôi resources.

```
Blue (current):  [v1] [v1] [v1] ← Traffic
Green (new):     [v2] [v2] [v2]

After testing:
Blue:            [v1] [v1] [v1]
Green:           [v2] [v2] [v2] ← Traffic shifted
```

> 💡 **Khi nào dùng:** Apps cần zero downtime và khả năng rollback instant. Ví dụ: banking, e-commerce.

### 3. Canary Deployment

**Cách hoạt động:** Deploy version mới cho một phần nhỏ traffic (1-10%). Monitor metrics. Nếu OK, tăng dần. Nếu lỗi, rollback ngay.

**Ưu điểm:** Phát hiện lỗi sớm với ít user bị ảnh hưởng.
**Nhược điểm:** Phức tạp hơn, cần monitoring tốt.

```
Stable: [v1] [v1] [v1] [v1] ← 90% traffic
Canary: [v2]                 ← 10% traffic

If OK:
[v2] [v2] [v2] [v2] [v2]     ← 100% traffic
```

> 💡 **Khi nào dùng:** Apps quan trọng, cần test với real traffic trước khi full rollout. Ví dụ: major feature releases.

---

## 🔧 GitHub Actions CD

**Đây là ví dụ CD pipeline đơn giản:** Mỗi khi push lên `main`, tự động build Docker image và deploy lên Kubernetes.

**Lưu ý:** Trong production thực tế, bạn nên:

- Test trước khi deploy
- Deploy qua staging trước production
- Có approval step cho production

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and push Docker
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}
      
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }}
```

**Giải thích:**

| Step | Ý nghĩa |
|------|---------|
| `on: push: branches: [main]` | Chỉ trigger khi push vào main |
| `myapp:${{ github.sha }}` | Tag image bằng commit SHA để track version |
| `kubectl set image` | Update Deployment với image mới, K8s sẽ rolling update |

---

## 📝 Tổng kết

✅ CD strategies  
✅ Rolling, Blue-Green, Canary  
✅ Automated deployments  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
