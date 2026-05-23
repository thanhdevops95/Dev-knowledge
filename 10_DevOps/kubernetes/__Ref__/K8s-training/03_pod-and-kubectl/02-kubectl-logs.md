# Bài #11 — Sử Dụng `kubectl logs`

> 🎯 Một trong những command **được dùng NHIỀU NHẤT** trong daily work với K8s — debug app bằng cách xem log.

---

## 📋 Metadata

- **Bài số:** #11
- **Module:** 03-pod-and-kubectl
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~3 phút
- **Prerequisites:** [Bài #8 — Pod là gì?](01-pod-la-gi.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Xem được log của 1 Pod (1 container)
- [ ] Stream log liên tục (giống `tail -f`)
- [ ] Xem log của container cụ thể trong multi-container Pod
- [ ] Biết các flag hữu ích: `-f`, `-c`, `--tail`, `--since`

---

## 📚 Nội Dung

### 1. Vì Sao Cần `kubectl logs`?

Khi developer **viết log** ra `stdout/stderr` (vd: `print()`, `console.log()`, `log.info()`), K8s **tự động capture** vào file trên Node. `kubectl logs` đọc file đó cho bạn xem.

```
┌─────── Pod ────────┐    kubelet    
│  ┌──────────────┐  │   capture     ┌─── /var/log/pods/... ───┐
│  │ App.py       │ ──→ stdout    →  │  json.log               │
│  │ print("...")  │ │            →  │  (rotated daily)        │
│  └──────────────┘  │              └─────────────────────────┘
└────────────────────┘                       ▲
                                              │ kubectl logs
                                              │
                                          Bạn (admin)
```

> ⚠️ **Quan trọng:** App phải log ra **stdout/stderr**, KHÔNG ghi vào file riêng (vì khi Pod chết, log mất).

---

### 2. Các Cú Pháp Cơ Bản

#### 🟢 Xem log toàn bộ Pod (đến hiện tại)

```bash
kubectl logs <pod-name>

# Ví dụ:
kubectl logs app-1
```

#### 🟢 Stream log liên tục (`-f` = follow)

Giống `tail -f` của Linux — log mới sẽ tự hiện ngay.

```bash
kubectl logs -f app-1
```

> 💡 Mỗi lần user truy cập web → log mới sẽ in ra terminal real-time. Nhấn `Ctrl+C` để thoát.

#### 🟢 Xem N dòng cuối

```bash
kubectl logs --tail=100 app-1
# Chỉ in 100 dòng cuối
```

#### 🟢 Xem log từ thời điểm cụ thể

```bash
kubectl logs --since=10m app-1     # 10 phút qua
kubectl logs --since=1h app-1      # 1 giờ qua
kubectl logs --since-time="2026-05-09T10:00:00Z" app-1
```

#### 🟢 Xem log của container CỤ THỂ trong multi-container Pod

```bash
kubectl logs <pod-name> -c <container-name>

# Ví dụ:
kubectl logs app-1 -c logger
kubectl logs app-1 -c logger -f
```

> 🔍 **Cách tìm tên container:** `kubectl describe pod app-1` → tìm phần `Containers:`

#### 🟢 Xem log của Pod đã crash trước đó

```bash
kubectl logs app-1 --previous
# hoặc
kubectl logs app-1 -p
```

> 💡 Đặc biệt hữu ích khi Pod restart vì crash — bạn cần xem log trước khi crash.

---

### 3. Combo Flag Hữu Ích

```bash
# Stream + chỉ 50 dòng cuối + giới hạn 10 phút
kubectl logs -f --tail=50 --since=10m app-1

# Stream tất cả container trong Pod (K8s 1.21+)
kubectl logs -f app-1 --all-containers=true

# Xem log Pod theo label selector (vd: app=frontend)
kubectl logs -l app=frontend --tail=100
```

---

## 💻 Hands-On / Demo

### Setup: Tạo Pod Có Log

```bash
# Tạo Pod nginx (có log truy cập sẵn)
kubectl run web --image=nginx --port=80

# Đợi Pod Running
kubectl get pods -w
# Ctrl+C khi thấy: web   1/1   Running   0   10s
```

### Test 1: Xem log

```bash
kubectl logs web
# (chưa có log vì chưa truy cập)
```

### Test 2: Generate traffic

```bash
# Trong terminal 1: stream log
kubectl logs -f web

# Trong terminal 2: port-forward
kubectl port-forward web 8080:80

# Trong terminal 3: gọi
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080
```

→ Terminal 1 sẽ in real-time:

```
172.17.0.1 - - [09/May/2026:12:00:01 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.81.0"
172.17.0.1 - - [09/May/2026:12:00:02 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.81.0"
172.17.0.1 - - [09/May/2026:12:00:03 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.81.0"
```

### Cleanup

```bash
kubectl delete pod web
```

---

## ⚠️ Lưu Ý

- 📝 App phải log ra **stdout/stderr**, đừng ghi file riêng (vì Pod chết → log mất).
- 🔥 Multi-container Pod **bắt buộc** dùng `-c <container>`, nếu không sẽ lỗi.
- 🔥 `kubectl logs --previous` (`-p`) cứu mạng khi debug crash loop.
- ⚠️ **Production:** dùng centralized logging (Loki, ELK, CloudWatch) thay vì `kubectl logs` mỗi lần.
- ⚠️ Log K8s rotate sau 1 size nhất định — log cũ sẽ mất nếu không ship đi đâu.

---

## ✅ Self-Check

1. **Lệnh nào stream log real-time?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl logs -f <pod-name>
   ```

   `-f` = follow (giống `tail -f`)
   </details>

2. **Pod có 2 container `app` và `logger`. Lệnh nào xem log của `logger`?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl logs <pod-name> -c logger
   ```

   </details>

3. **Pod vừa crash, bạn muốn xem log trước khi crash?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl logs <pod-name> --previous
   # hoặc
   kubectl logs <pod-name> -p
   ```

   </details>

4. **App ghi log vào file `/app/logs/app.log` thay vì stdout. Có thể `kubectl logs` được không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG** — `kubectl logs` chỉ đọc stdout/stderr. Phải sửa app log ra stdout, hoặc `kubectl exec` vào Pod xem file thủ công.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #8 — Pod là gì?](01-pod-la-gi.md)
- ➡️ [Bài #12 — kubectl exec](03-kubectl-exec.md)

### Tài Nguyên

- 📖 [kubectl logs reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- 📖 [Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- 📺 Video gốc: `Decopy_✅ #11 _ Sử Dụng kubectl logs_captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"`kubectl logs` rất tương tự `docker logs` — bạn nào đã quen Docker thì sẽ thấy quen ngay."*

> 💬 *"Nếu Pod có nhiều container, các bạn PHẢI chỉ định `-c <container-name>`, nếu không sẽ lỗi."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
