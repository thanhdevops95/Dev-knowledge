# 🔌 Embedded & IoT — Lập trình hệ nhúng và Internet of Things

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 22/06/2026

> 🎯 *Lập trình hệ nhúng + IoT: máy tính chuyên dụng tài nguyên hạn chế, chạy real-time. Học vi điều khiển + GPIO, giao tiếp UART/I2C/SPI, RTOS (FreeRTOS task/queue), rồi kết nối thiết bị lên cloud qua MQTT. CÓ code chạy được (Arduino C++, FreeRTOS trên ESP32, MQTT với PubSubClient), nhiều sơ đồ + dự án xuyên suốt: đọc nhiệt độ → bật quạt → đẩy lên cloud.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Phân biệt **embedded vs IoT**, MCU vs vi xử lý có OS, bare-metal vs RTOS vs Linux nhúng
- [x] Điều khiển **GPIO**: digital I/O, pull-up/down, ADC đọc cảm biến analog, PWM (code Arduino)
- [x] Chọn đúng **giao tiếp** UART / I2C / SPI theo nhu cầu (số dây, tốc độ, số thiết bị)
- [x] Hiểu **real-time + RTOS**: task, scheduler ưu tiên, semaphore/mutex/**queue** (FreeRTOS trên ESP32)
- [x] **Kết nối IoT lên cloud** qua **MQTT** (pub/sub, broker, QoS) + bảo mật (TLS, không hard-code secret, OTA)

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Embedded & IoT là gì?`](./lessons/01_basic/00_what-is-embedded-iot.md) | ✅ | Embedded vs IoT, MCU vs Linux nhúng, kiến trúc device→gateway→cloud. |
| **01** | [`Vi điều khiển & GPIO`](./lessons/01_basic/01_microcontrollers-and-gpio.md) | ✅ | Cấu tạo MCU, digital I/O, pull-up/down, ADC, PWM (Arduino C++). |
| **02** | [`Giao tiếp: UART, I2C, SPI`](./lessons/01_basic/02_communication-protocols.md) | ✅ | So sánh 3 bus, đọc cảm biến I2C (Wire), khi nào dùng cái nào. |
| **03** | [`RTOS & lập trình real-time`](./lessons/01_basic/03_rtos-and-realtime.md) | ✅ | Hard/soft real-time, task/scheduler, semaphore/mutex/queue, FreeRTOS/ESP32. |
| **04** | [`Kết nối IoT lên Cloud`](./lessons/01_basic/04_connecting-to-the-cloud.md) | ✅ | MQTT vs HTTP, pub/sub, ESP32+WiFi+PubSubClient, TLS, OTA, bảo mật. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Có một board **ESP32** (rẻ, có sẵn WiFi) thì học hiệu quả nhất vì code các bài chạy được trên đó. Người mới: nắm chắc [01 (GPIO)](./lessons/01_basic/01_microcontrollers-and-gpio.md) + [02 (giao tiếp)](./lessons/01_basic/02_communication-protocols.md) trước; [03 (RTOS)](./lessons/01_basic/03_rtos-and-realtime.md) hơi nâng cao, đọc khi đã quen super-loop. Chú ý mục **bảo mật** ở [04](./lessons/01_basic/04_connecting-to-the-cloud.md) — IoT là mục tiêu tấn công phổ biến.

## 🔗 Liên kết cụm liên quan

- [03_languages](../../03_languages/) — C/C++ nền tảng cho lập trình nhúng.
- [robotics](../robotics/) — robot = embedded + cảm biến + cơ cấu chấp hành.
- [05_networking](../../05_networking/) — TCP/IP, TLS, MQTT chạy trên nền mạng.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (22/06/2026)** — Hoàn thiện cụm **Basic 5/5** (embedded/IoT là gì + GPIO + UART/I2C/SPI + RTOS/real-time + kết nối cloud MQTT).
