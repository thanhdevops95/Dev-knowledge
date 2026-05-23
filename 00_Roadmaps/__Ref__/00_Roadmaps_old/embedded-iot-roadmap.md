# 🔌 Lộ trình Embedded & IoT Engineer

> `[BEGINNER → ADVANCED]` — Xem trước [Tổng quan Lộ trình](./00-overview.md)

---

## Tại sao Embedded & IoT?

Embedded systems chạy trong mọi thứ xung quanh bạn — từ remote TV, máy giặt, đến xe ô tô và vệ tinh. IoT kết nối hàng tỷ thiết bị này lên internet, tạo ra "thế giới thông minh". Nếu web developer xây nhà trên đất, thì embedded engineer **xây nền móng** — nơi mỗi byte bộ nhớ và mỗi millisecond đều quan trọng.

Đây là lĩnh vực kết hợp phần cứng và phần mềm. Bạn sẽ làm việc gần với "kim loại" (bare metal) hơn bất kỳ developer nào khác, và hiểu sâu cách máy tính thực sự hoạt động.

---

## Sơ đồ lộ trình

```
C/C++ Basics
    │
    ▼
Microcontrollers (Arduino, STM32, ESP32)
    │
    ├──► RTOS (FreeRTOS, Zephyr)
    │
    ├──► Linux Embedded (Yocto, Buildroot)
    │
    ▼
IoT Protocols (MQTT, CoAP, BLE)
    │
    ▼
IoT Platforms (AWS IoT, Azure IoT)
    │
    ▼
Linux Kernel & Device Drivers (Advanced)
```

---

## Giai đoạn 1 — C/C++ cơ bản

- [ ] C cơ bản → [../05-Languages/c/01-c-basics.md](../05-Languages/c/01-c-basics.md)
- [ ] C++ cơ bản → [../05-Languages/cpp/01-cpp-basics.md](../05-Languages/cpp/01-cpp-basics.md)
- [ ] Pointers, Memory management, Bit manipulation
- [ ] Data structures in C (linked list, queue, ring buffer)
- [ ] Makefile & cross-compilation basics

---

## Giai đoạn 2 — Microcontrollers

- [ ] MCU basics → [../19-Embedded-IoT/embedded/01-microcontrollers-basics.md](../19-Embedded-IoT/embedded/01-microcontrollers-basics.md)
- [ ] GPIO, Interrupts, Timers
- [ ] Communication protocols: UART, SPI, I2C
- [ ] ADC/DAC, PWM
- [ ] Hands-on: Arduino → STM32 → ESP32

---

## Giai đoạn 3 — RTOS

- [ ] RTOS fundamentals → [../19-Embedded-IoT/embedded/02-rtos-basics.md](../19-Embedded-IoT/embedded/02-rtos-basics.md)
- [ ] Tasks, Scheduling, Priority inversion
- [ ] Semaphores, Mutexes, Queues
- [ ] FreeRTOS hoặc Zephyr RTOS
- [ ] Real-time constraints & deadline analysis

---

## Giai đoạn 4 — Linux Embedded

- [ ] Linux Embedded basics → [../19-Embedded-IoT/embedded/03-linux-embedded-basics.md](../19-Embedded-IoT/embedded/03-linux-embedded-basics.md)
- [ ] Cross-compilation toolchain
- [ ] Yocto Project / Buildroot
- [ ] U-Boot bootloader
- [ ] Device Tree cơ bản

---

## Giai đoạn 5 — IoT Protocols

- [ ] MQTT cơ bản → [../19-Embedded-IoT/iot/01-mqtt-basics.md](../19-Embedded-IoT/iot/01-mqtt-basics.md)
- [ ] CoAP, HTTP cho IoT
- [ ] Bluetooth Low Energy (BLE)
- [ ] LoRa / LoRaWAN cho long-range IoT
- [ ] OTA (Over-The-Air) firmware updates

---

## Giai đoạn 6 — IoT Platforms

- [ ] IoT platforms cơ bản → [../19-Embedded-IoT/iot/02-iot-platforms-basics.md](../19-Embedded-IoT/iot/02-iot-platforms-basics.md)
- [ ] AWS IoT Core, Azure IoT Hub
- [ ] Edge computing (AWS Greengrass)
- [ ] Data pipeline: Device → Gateway → Cloud → Dashboard
- [ ] Security: TLS, Certificate-based auth, Secure boot

---

## Giai đoạn 7 — Linux Kernel (Nâng cao)

- [ ] Linux Kernel deep dive → [../19-Embedded-IoT/systems/01-linux-kernel-deep-dive.md](../19-Embedded-IoT/systems/01-linux-kernel-deep-dive.md)
- [ ] Kernel modules & Device drivers
- [ ] Memory management (virtual memory, DMA)
- [ ] Kernel debugging (ftrace, kgdb)

---

## 📦 Project thực hành

| Giai đoạn | Project |
|---|---|
| Sau MCU | LED blink → Sensor reader → LCD display (Arduino/ESP32) |
| Sau RTOS | Multi-task system: sensor + display + communication |
| Sau IoT | Weather station gửi data qua MQTT lên dashboard |
| Sau Platform | Smart home system (ESP32 + MQTT + AWS IoT + Web UI) |
| Nâng cao | Custom Linux image cho Raspberry Pi với Yocto |

---

## 📚 Tài nguyên

- [FreeRTOS Docs](https://www.freertos.org/Documentation/RTOS_book.html) — Tài liệu RTOS chính thức
- [Embedded Artistry](https://embeddedartistry.com/) — Blog chất lượng cao về embedded
- [Yocto Project Docs](https://docs.yoctoproject.org/) — Build custom Linux distros
- [MQTT.org](https://mqtt.org/) — IoT messaging protocol specification
- [Nand2Tetris](https://www.nand2tetris.org/) — Hiểu máy tính từ transistor đến OS
