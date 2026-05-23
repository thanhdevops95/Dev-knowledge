# Bài 38 — Ingress

## Tiên quyết

- Ingress controller đã cài. Với Minikube:
  ```bash
  minikube addons enable ingress
  ```

## Lệnh thủ công

```bash
# 1. Apply Ingress
kubectl apply -f ingress.yaml

# 2. Lấy IP để thêm vào /etc/hosts
minikube ip
# Output: ví dụ 192.168.49.2

# 3. Thêm vào /etc/hosts (cần sudo)
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts

# 4. Test
curl http://myapp.local
curl http://myapp.local/health
```

## Kết quả mong đợi

- `curl http://myapp.local` trả response từ myapp.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `Could not resolve host: myapp.local` | Thêm vào `/etc/hosts` chưa hoặc sai IP |
| 502/504 | Ingress đã route nhưng backend Service không có endpoint — `kubectl get endpoints` |

## Bài kế tiếp

```bash
cp -r ../38-ingress ../39-statefulset
cd ../39-statefulset
```
