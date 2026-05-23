# 🔥 Kubernetes Monitoring — Giám Sát Và Báo Động Lỗi K8s

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Khi bạn có hàng ngàn dịch vụ trong K8s, thay vì dò dẫm trong mù quáng, bạn sẽ thiết lập màn hình theo dõi siêu nhạy để tự phản ứng trước sự cố.
> **Prerequisite:** `09-DevOps/kubernetes/01-kubernetes-basics.md`

---

## Tại sao K8s phải có công cụ Monitoring chuyên nghiệp?

Ở máy chủ truyền thống (như 1 server nhỏ lẻ cài Linux), bạn có thể chạy dòng lệnh `top` hay `htop` để kiểm tra RAM, CPU, và dùng `tail -f` xem Log. 
Nhưng K8s có cấu trúc phân tầng tĩnh và động quá lớn (Bao gồm hàng trăm cái Node, mỗi Pod chạy trên một IP ngẫu nhiên và liên tục tự diệt tái sinh). Bạn không thể kết nối tới các Node và truy xuất Log bằng cách gõ Console vì chúng hoàn toàn tự động đổi trạng thái và mã mạng sinh học mỗi phút. K8s sẽ là "hộp đen" nếu bạn không có màn hình đo hệ thống (Observability).

---

## 1. Phương Pháp Metrics Lấy Thông Số (Prometheus + Grafana)

**Prometheus** thường được sử dụng như là trình theo dõi gốc và phổ biến nhất ở kiến trúc Kubernetes do đặc tính siêu rà cấu. Phương thức lấy tham số cắm đo ở máy của Prometheus khác biệt với các ứng dụng cũ. Nó áp dụng phương pháp đo **PULL Model** trên toàn mạng cài.  

Công cụ sẽ thực hiện hai cài lưới tính:
1. `Kube-state-metrics`: K8s đã cài một trạm máy nhỏ tính xuất liên tục đo tham số đếm luồng (Báo cáo tổng số Pod bị crash trên toàn hệ). 
2. `Prometheus`: Sẽ định kỳ 10 giây đi dạo chạy chọc chọc qua các cổng mạng Endpoint của kĩ thuật số Kube-state-metrics bằng câu truy xuất thông http kết `/metrics`. Rút tham mạng đo báo đếm số bằng mạng biểu về CSDL biểu máy chủ theo cấu trình thời gian (Time-series Database). Kĩ thuật này rất nhẹ và không gây nặng mạng cho K8s hệ thay vì mỗi hệ Pod tự bắn dữ về báo Cấu Tệp.

**Grafana:** Là một nền tảng chuyên kết rào đồ thị hóa nhận số liệu từ CSDL của Prometheus để vẽ cái thông thành Biểu bản Đẹp và cấu bảng Rẽ Máy mảng Hệ Rào Trực Báo Chặn Mảng Báo (AlertManager rẽ Telegram/Slack).

---

## 2. Hệ Quản Trị Trung Tâm Trạm Log Phân Tán (ELK/EFK Stack)

Log ở mạng K8s có vòng đời cũng ngắn và xóa tệp trống ngay theo cái Pod ở đó. Nếu Pod web của Java nổ ứng ném ra màn 1 file Error 500 mạng tĩnh, rồi ứng Nổ K8s tử Diệt Mạng Phủ Sinh cài 1 Pod cấu khác bù tạo Mới. Lưới log chứa 500 lỗi đó mất vĩnh Hệ bộ! 

Phải có 1 hệ sinh Trạm Log mạng Tập Cài: **Elasticsearch, Fluentd, Kibana (EFK)**
Một tiến trình máy nền nhỏ mang tên Fluentd sẽ cài cài mạng cài DaemonSet trên mọi cấu máy mẹ gốc Worker cài mạng Node Thực. Mỗi khi chạy chạy có 1 Pod cài bất chạy kì Mạng cấu phun Chữ Lỗi tải log, con Fluentd tự rào đứng đó Nhặt thông tin rẽ Lưới chữ Tệp và ném Đẩy tất Khối vào cái Máy Kho Tìm Giao Khối Tìm Kiếm Lệnh Siêu Tốc Hệ Khổng ứng Lưới Elasticsearch.

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình sử dụng bộ lệnh `kubectl logs` thiết qua mảng rẽ dòng gọi lệnh hệBash cục cài để theo truy cấu phân dò luồng lỗi Hệ Lớn Trực K8s cấu Cụm Dài ứng dụng trên Mảng Từng cấu Pod một. | Sử Dụng giao kết ứng Truy CSDL Đám tìm Hệ Mảng Kibana Căn hoặc Màng Elasticsearch cài nhập Rào lệnh Tìm Mảng Trục Khóa Hệ (Ví Dụ `level: ERROR AND app: NodeBackend`). | Dòng lưới Lệnh Bash `kubectl logs` trên mạng cục Mảng chỉ hỗ lệnh đọc được mảng 1 tệp vỏ Pod ảo. Để truy báo Mảng 1 dòng thông rẽ mảng chữ mạng Trạm trên hệ Cụm hệ Cài 100 ảo Máy Trạm Chạy ứng Giao, Sử Bash sẽ Rào Mất Đám Đứt Nền ứng Tốn Trạm Gọi Kì Cấu Phủ Thiết. Hệ ELK/EFK gom cài 100 Giao lưới tệp thông qua Tìm cấu 1 Mệnh Mạng Siêu Bảng Tốc Lệnh Rẽ Thiết. |
| 2 | Mở Thiết Cài Cấu ứng Đặt Gọi Prometheus Mạng Truy Cấu Trạm Giữ thông Mọi Thông Hệ Lưới Mảng Thiết Lệnh Trạm Rẽ Trong Vòng Chạy Cấp Báo Lịch Số Thời Giao Gian Phân Tính Năm Rẽ Định Tháng Cài. | Áp Hàm Cấu Chỉnh Rào Lưới Giới Tệp Định Hạn Lưu Số Giao Liệu Báo Nén Chỉ Mảng Ở Đám Tối Tham Rẽ 15 Đám Thiết Ngày (Lệnh Cờ: `--storage.tsdb.retention.time=15d`). | Ứng Dụng Nén Cấu Prometheus Cài Không Mạng Giải Giao Cấu Pháp Rào Truy Dụng Cấu Dữ Trữ Lưu Bảng Lâu Thiết Vừa Trạm Nén Lịch Trực Rẽ Báo Truy Sử Cứu Dài Hệ Kì. Nếu Bảng Lưu lưới Lâu Gắn Sẽ Lỗi Phủ Cài Xóa OOM Ngập Trạm Ổ Cụm Ảo Cứng Giao K8s Rẽ (Dùng Hệ Thanos Nếu Chọn Cấu Thiết Lưu Giao Mảng Dữ Nhiều Thông Tháng Mạch). |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết lập Cài Mảng Helm lưới Báo Giao Ứng Dụng Phân Lập Bằng Mệnh Chuẩn Định Gói Kube-Prometheus-Stack (Sử Thiết Ở Kho Tệp Cộng Helm rào Hub). Dùng mảng lệnh tạo Cài Gọi Lập Phủ Bản Test Chạy Lên Minikube ảo hệ Lập Thiết Giao. Cài Và Chọn Dùng Cổng Mạng NodePort Trạm Lập Chạy Gọi Cổng để Mở Tới Gọi Mạng Vào Giao Truy Bảng Graphic Của Báo Lệnh Grafana Thiết Cài Ảo Ở Trình Gắn Cục Bộ Lệnh Mạng Chạy (Lệnh Cài Username/Password Giao: admin/prom-operator).
- [ ] **Bài 2:** Thiết Cấu Tạo Tạo Báo Bảng Thử Dashboard Mạng Mảng Xem Bảng Nén Trên Đồ Lệnh Đồ Thị Đám Mạng Mạch Nền Grafana Thiết Lập Cài Biểu Cứ Thiết CPU Của Thiết Toàn Thông Bộ Mạch Giao Phân Node Trạm Rẽ Mạch Nằm Gắn Trong Ứng Phân Hệ Cấu Cluster.  

---

## Tài nguyên thêm
- [Prometheus Architecture Official Setup](https://prometheus.io/docs/introduction/overview/) — Khái cấu cài mạng nền tảng lưới thông quản báo lưới đo cấu số máy Gốc Giao Cài Giao hệ trạm Ứng rẽ trạm hệ Prometheus.
- [EFK Stack Setup Kubernetes Log Elastic](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html) — Giao Tích Trạng Lập Mảng Trình Mạch Cấu Cấu Truy Định Giao Bảng Cấu Rẽ Ảo Cài Elastic Log Phục Cấu Mảng Lưới Trạm.
