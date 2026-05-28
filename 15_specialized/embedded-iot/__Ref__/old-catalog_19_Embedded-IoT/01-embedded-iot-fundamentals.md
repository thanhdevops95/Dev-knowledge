# 🔌 Embedded & IoT — Hệ thống nhúng

> `[BEGINNER → INTERMEDIATE]` — Lập trình cho phần cứng thực tế

---

## Embedded là gì?

**Hệ thống nhúng** = máy tính nhỏ được tích hợp vào thiết bị, thực hiện 1 nhiệm vụ cụ thể.

```
Ví dụ hàng ngày:
• Máy giặt: MCU đọc nút bấm → điều khiển motor + van nước
• Remote TV: MCU đọc nút → gửi tín hiệu IR
• Xe hơi: 50-100 ECUs (Engine Control Units)
• Smart home: ESP32 đọc sensor → gửi data → cloud → app

IoT (Internet of Things):
  Thiết bị nhúng + Kết nối Internet + Cloud
  Sensor → MCU → WiFi/BLE → Cloud → Dashboard/App
```

---

## 1. Hardware cơ bản

```
┌─────────────────────────────────────────┐
│          Microcontroller (MCU)          │
│  ┌──────┐  ┌──────┐  ┌──────┐         │
│  │ CPU  │  │ RAM  │  │ Flash│         │
│  │      │  │ (KB) │  │ (MB) │         │
│  └──────┘  └──────┘  └──────┘         │
│  ┌──────┐  ┌──────┐  ┌──────┐         │
│  │ GPIO │  │ UART │  │ I2C  │         │
│  │      │  │ SPI  │  │ ADC  │         │
│  └──┬───┘  └──┬───┘  └──┬───┘         │
└─────┼─────────┼─────────┼──────────────┘
      │         │         │
   LED/Button  Serial   Sensors
   Motor       Display  (temp, humidity)
```

| Board | CPU | RAM | WiFi | Giá | Phù hợp |
|---|---|---|---|---|---|
| **Arduino Uno** | ATmega328P | 2KB | ❌ | ~$5 | Học cơ bản |
| **ESP32** | Xtensa 240MHz | 520KB | ✅+BLE | ~$3 | IoT ⭐ |
| **Raspberry Pi Pico** | RP2040 | 264KB | ✅ (W) | ~$6 | MicroPython |
| **Raspberry Pi 4** | ARM Cortex-A72 | 1-8GB | ✅ | ~$35 | Linux, AI edge |
| **STM32** | ARM Cortex-M | 64-1024KB | Tùy | ~$5 | Professional |

---

## 2. Arduino — Bắt đầu

```cpp
// Arduino — Blink LED
const int LED_PIN = 13;
const int BUTTON_PIN = 2;

void setup() {
    pinMode(LED_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    Serial.begin(9600);
}

void loop() {
    if (digitalRead(BUTTON_PIN) == LOW) {
        digitalWrite(LED_PIN, HIGH);
        Serial.println("Button pressed!");
    } else {
        digitalWrite(LED_PIN, LOW);
    }
    delay(50);  // Debounce
}
```

### Đọc Sensor

```cpp
// Đọc nhiệt độ từ DHT22
#include <DHT.h>

DHT dht(4, DHT22);

void setup() {
    Serial.begin(9600);
    dht.begin();
}

void loop() {
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (!isnan(temp) && !isnan(humidity)) {
        Serial.printf("Temp: %.1f°C, Humidity: %.1f%%\n", temp, humidity);
    }
    delay(2000);
}
```

---

## 3. ESP32 + MicroPython — IoT

```python
# MicroPython trên ESP32

# Blink LED
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(not led.value())
    time.sleep(0.5)

# WiFi connection
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('WiFi_Name', 'password')

while not wlan.isconnected():
    time.sleep(1)

print('Connected:', wlan.ifconfig())

# HTTP Server — điều khiển LED qua web
import socket

html = """
<html><body>
<h1>ESP32 Control</h1>
<a href="/on"><button>LED ON</button></a>
<a href="/off"><button>LED OFF</button></a>
</body></html>
"""

s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()

    if '/on' in request:
        led.value(1)
    elif '/off' in request:
        led.value(0)

    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html)
    conn.close()
```

---

## 4. MQTT — Giao thức IoT

```
MQTT = Message Queuing Telemetry Transport

Lightweight, publish/subscribe, cho mạng không ổn định

Sensor ──publish──► MQTT Broker ──subscribe──► Dashboard
                    (Mosquitto)                (Grafana)
                         │
                    ──subscribe──► Mobile App
                    ──subscribe──► Cloud (AWS IoT)
```

```python
# ESP32 gửi data qua MQTT
from umqtt.simple import MQTTClient

client = MQTTClient("esp32_01", "broker.hivemq.com")
client.connect()

while True:
    temp = read_temperature()
    client.publish("home/living/temp", str(temp))
    time.sleep(60)

# Server nhận data (Python)
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect("broker.hivemq.com")
client.subscribe("home/#")  # Tất cả topics bắt đầu bằng home/
client.loop_forever()
```

---

## 5. IoT Architecture

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Sensors │──►│   Edge   │──►│  Cloud   │──►│Dashboard │
│ Actuators│   │ Gateway  │   │ Platform │   │ Mobile   │
│          │   │(ESP32/Pi)│   │(AWS IoT) │   │  App     │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
 Temperature    Process        Store          Visualize
 Humidity       Filter         Analyze        Alert
 Motion         Aggregate      ML/AI          Control

Protocols:
  Device ↔ Gateway:  MQTT, BLE, Zigbee, LoRa
  Gateway ↔ Cloud:   MQTT, HTTPS, WebSocket
  Cloud ↔ App:       REST API, WebSocket, GraphQL
```

---

## 6. Raspberry Pi — Linux cho IoT

```python
# Raspberry Pi — GPIO với Python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)     # LED
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button

try:
    while True:
        if GPIO.input(24) == GPIO.LOW:
            GPIO.output(18, GPIO.HIGH)
            print("Button pressed!")
        else:
            GPIO.output(18, GPIO.LOW)
        time.sleep(0.1)
finally:
    GPIO.cleanup()

# Camera + AI (edge computing)
from picamera2 import Picamera2
import cv2

camera = Picamera2()
camera.start()

while True:
    frame = camera.capture_array()
    # Run ML model (TensorFlow Lite)
    result = model.predict(frame)
    if result == "person":
        send_alert("Phát hiện người!")
```

---

## Các lỗi thường gặp

```
❌ Sai: Dùng delay() blocking → MCU không làm gì khác
✅ Đúng: Dùng millis() non-blocking hoặc RTOS tasks

❌ Sai: Truyền data IoT không mã hóa
✅ Đúng: MQTT + TLS, HTTPS cho mọi communication

❌ Sai: Raspberry Pi cho task đơn giản (blink LED)
✅ Đúng: Arduino/ESP32 cho task nhỏ, RPi cho AI/camera/Linux
```

---

## Bài tập thực hành

- [ ] Arduino/ESP32: đọc sensor nhiệt độ → hiển thị Serial
- [ ] ESP32 + WiFi: web server điều khiển LED từ browser
- [ ] MQTT: ESP32 publish sensor data → Python subscriber hiển thị
- [ ] Raspberry Pi: camera + face detection (OpenCV)

---

## Tài nguyên thêm

- [Arduino Docs](https://docs.arduino.cc/) — Official tutorials
- [ESP32 Guide (Random Nerd)](https://randomnerdtutorials.com/) — Tutorials cực tốt
- [MicroPython Docs](https://docs.micropython.org/) — Python cho MCU
