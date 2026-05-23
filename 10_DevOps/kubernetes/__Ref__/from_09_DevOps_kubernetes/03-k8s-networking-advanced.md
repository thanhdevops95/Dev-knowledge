# 🔥 Kubernetes Networking — Mạng Lưới K8s Chuyên Sâu

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Hiểu cách ứng dụng nội bộ từ các cỗ máy Kubernetes trong không gian mạng kết nối ra hệ thống bên ngoài.
> **Prerequisite:** `09-DevOps/kubernetes/01-kubernetes-basics.md`

---

## 1. Mạng Dịch Vụ Cục Bộ (ClusterIP Service)

`ClusterIP` là kiểu mạng mặc định và chiếm tần suất sử dụng cao nhất. 
Nó tạo ra danh tính mạng tên cục bộ không thể gọi được từ máy điện thoại hay trình duyệt người dùng bên ngoài Internet. Nó chỉ giúp các máy ứng dụng ở bên trong hệ thống tự nói chuyện qua lại với nhau.

- Ví dụ: Ứng dụng Backend API gọi cấu hình tên cục bộ `redis-service:6379` để gửi dữ liệu lưu tạm. Khách hàng bên ngoài không thể thọc dò trực tiếp vào mạng Redis chặn cổng an toàn tuyệt đối.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  type: ClusterIP # (Chỉ lưu hành mạng máy nội bộ)
  selector:
    app: redis
  ports:
    - port: 6379 
```

---

## 2. Cổng Kết Nối Ra Ngoài (NodePort và LoadBalancer)

Nếu muốn đưa ứng dụng ra bên ngoài máy trạm, ta có 2 tính năng cơ sở dịch thuật cổng.

- **NodePort:** K8s lấy ứng dụng và mở chọc một lỗ hổng trên cổng mạng vật lý của cái máy Node (giới hạn từ số 30000 - 32767).
- **LoadBalancer:** Lệnh trực tiếp hệ thống đám mây (AWS/GCP) cấp 1 chuỗi IP thiết bị mạng chuyên dụng ngoài hệ thống. Hướng luồng đường dẫn chạy từ môi trường công cộng Internet vào mạng bộ K8s. Tuy nhiên, nếu bạn chạy 10 dự án (Web Đọc Báo, Web Game), việc mỗi dự án xin 1 LoadBalancer rất đắt mỏ (có thể đến 20$/IP/Tháng).

---

## 3. Ingress Control — Trạm Thu Phí Lưu Lượng

Thay vì thuê 10 LoadBalancer tính phí ở đám mây cho 10 dịch vụ, **Ingress Control** là giải pháp tối ưu. Nó hoạt động như tấm thẻ ngã tư chia đường hầm. Bạn chỉ thuê 1 cục LoadBalancer của đám mây đưa IP duy nhất. Hệ thống Ingress Controller (thường cài Nginx/Traefik) chạy ngầm kiểm soát miền. 

Khi URL gõ vào trình duyệt từ người dùng là `api.congty.com`, Ingress dẫn ngầm vào (ClusterIP Backend).
Nếu gõ URL là `congty.com`, Ingress dẫn ngầm vào hệ thống (ClusterIP ReactJS).

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: he-thong-ingress
spec:
  rules:
  - host: api.congty.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service: # Điều chuyển qua luồng tên dịch vụ nội bộ
            name: backend-api-clusterip 
            port: 
              number: 8080
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Mở NodePort thẳng rẽ ra ngoài cấp thiết mạng Public cho máy cơ sở xử lý hệ cơ sở dữ liệu phân dòng Database. | Luôn để Database khóa chặt ở rào trong hệ Type ClusterIP. | Hệ NodePort mở xuyên luồng thủng mạng từ Cụm Máy của hệ K8s. Các bộ scan IP hệ Hacker mã rác sẽ nhảy dò trực tiếp rà quét cổng mạng đánh thủng dữ liệu DB lộ thiên. |
| 2 | Cấu kết tập tin thông báo Ingress chặn mạng không hoạt động nhưng không cài ứng dụng lõi Ingress Controller ở máy gốc. | Bắt buộc chạy cài đặt Ingress Controller (như Nginx-Ingress qua Helm) vào Cụm trước khi gọi API Ingress yaml của K8s. | Khai báo file yaml `kind: Ingress` chỉ là tờ đơn viết giấy xin đường. Nginx Ingress Controller là thằng công an giao thông thực tế. Không lập trình tạo Công an bằng gói Helm thì Ingress yaml không tự hoạt động. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cài hệ thống cấu hình bộ mạng Nginx-Ingress qua bản Helm lên kho chạy Minikube tại môi trường của bạn (`minikube addons enable ingress`).
- [ ] **Bài 2:** Thiết kế tệp tin thiết lập YAML chứa 2 khối ứng dụng web trơn phân 2 cổng (Trang chữ A dùng Echo và chữ B dùng httpd-alpine). Tạo 2 ClusterIP Service bảo kê cho 2 ứng dụng.
- [ ] **Bài 3:** Thiết kế tập `Ingress` yaml để phân bổ cấu máy nếu địa chỉ máy ảo gọi miền Localhost `/tao_a` sẽ hiển trang ứng dụng A, gọi đường dẫn trỏ tham số cổng `/tao_b` sẽ mở xem trên mạng chữ ứng dụng trang B.

---

## Tài nguyên thêm
- [K8S Ingress Document](https://kubernetes.io/docs/concepts/services-networking/ingress/) — Đồ thị và tài liệu về nguyên phân phối luồng URL mảng dẫn mạng ảo.
- [Service Types ClusterIP vs NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) — Công cụ hệ thống tra thông số phân lập mở loại hình mạng truy xuất Cloud ngoài hệ.
