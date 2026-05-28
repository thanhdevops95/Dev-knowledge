# Bài 22 — Multi-stage Build: tối ưu image

> **Loại bài:** thêm `Dockerfile.multi`, build `myapp:5.0-slim`, so sánh size.
> **Snapshot trước:** copy từ `21-network-redis/`.

## File mới

`myapp/Dockerfile.multi` — Dockerfile 2 stage:
- Stage `builder`: dùng image `python:3.11` (lớn, có dev tools) để pip install
- Stage runtime: dùng `python:3.11-slim`, chỉ copy site-packages từ builder

## Lệnh thủ công

```bash
cd myapp

# 1. Build với Dockerfile multi-stage
docker build -t myapp:5.0-slim -f Dockerfile.multi .

# 2. So sánh size
docker images myapp
```

## Kết quả mong đợi

```
REPOSITORY   TAG          IMAGE ID       CREATED          SIZE
myapp        5.0-slim     ...           a few seconds    ~140MB
myapp        5.0          ...           ago              ~145MB
myapp        4.0          ...           ago              ~140MB
...
```

> **Lưu ý:** Với app Python đơn giản, multi-stage tiết kiệm ~5-10MB. Với app Go/Rust, multi-stage có thể giảm 90%+ (binary cuối ~10MB từ image build 1GB).

## Câu hỏi

- Multi-stage nhỏ hơn bao nhiêu? *(với app này: vài MB; với compiled languages: rất lớn)*
- Khi nào nên dùng?
  - App cần build tool ở stage builder (gcc, npm, cargo)
  - Muốn image runtime tối thiểu (production)

## Bài kế tiếp

```bash
cp -r ../22-multi-stage ../23-compose
cd ../23-compose
```
