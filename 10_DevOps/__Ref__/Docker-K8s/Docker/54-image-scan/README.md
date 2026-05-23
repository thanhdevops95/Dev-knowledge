# Bài 54 — Image Scanning: `trivy` + `docker scout` 🔴

> **Loại bài:** học tool ngoài, không sửa source.
> **Snapshot trước:** copy từ `53-entrypoint-signal/` (cần image `myapp:safe` từ Bài 51).

## Mục tiêu

Trước khi `docker push` lên registry, phải scan image để biết:

- Có CVE **CRITICAL/HIGH** nào không?
- CVE đó đã có **fixed version** chưa?
- App có rò rỉ secret (`.env`, API key) trong layer không?

## 2 tool chính

| Tool | Ưu | Nhược |
|------|----|-------|
| **`docker scout`** | Cài sẵn trong Docker Desktop, output đẹp | Cần Docker Hub login; free cho repo public |
| **`trivy`** | Open source, scan vuln + misconfig + secret, output JSON/SARIF tốt cho CI | Cài thêm; DB lần đầu mất 1-2 phút |

## File trong thư mục này

```
54-image-scan/
└── README.md           ← chỉ README, dùng image myapp:safe từ Bài 51
```

Nếu chưa có image:

```bash
cd ../51-secure-image/myapp && docker build -t myapp:safe . && cd -
```

## Lệnh thủ công

### Phần A — Docker Scout (built-in)

```bash
# 1. Login Docker Hub (Scout cần auth)
docker login

# 2. Quick view: bảng summary CVE theo severity
docker scout quickview myapp:safe

# 3. Chi tiết từng CVE
docker scout cves myapp:safe

# 4. Gợi ý base image ít CVE hơn
docker scout recommendations myapp:safe

# 5. So sánh 2 image
docker scout compare myapp:safe --to myapp:6.0
```

### Phần B — Trivy (open source)

```bash
# 6. Cài Trivy
# macOS:
brew install aquasecurity/trivy/trivy
# Linux Debian/Ubuntu:
# sudo apt-get install -y trivy   (hoặc xem trivy.dev/docs/install)

# 7. Scan image — full report
trivy image myapp:safe

# 8. Chỉ HIGH/CRITICAL
trivy image --severity HIGH,CRITICAL myapp:safe

# 9. Bỏ CVE chưa có fix (giảm noise)
trivy image --ignore-unfixed myapp:safe

# 10. Scan filesystem (TRƯỚC khi build) — phát hiện secret/misconfig sớm
cd ../51-secure-image/myapp
trivy fs --scanners vuln,misconfig,secret .
cd -
```

### Phần C — Output cho CI/CD

```bash
# 11. JSON cho parsing
trivy image --format json --output report.json myapp:safe

# 12. SARIF để upload lên GitHub Code Scanning
trivy image --format sarif --output report.sarif myapp:safe

# 13. Fail build nếu có CRITICAL (exit code khác 0)
trivy image --exit-code 1 --severity CRITICAL myapp:safe
echo "Exit code: $?"
```

### Phần D — GitHub Actions sample

```yaml
# .github/workflows/scan.yml
name: Scan image
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: docker build -t myapp:safe ./51-secure-image/myapp
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:safe'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'              # fail build nếu có CVE
          format: 'sarif'
          output: 'trivy-results.sarif'
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

## Kết quả mong đợi

- `docker scout quickview` in bảng `C / H / M / L / ?` (Critical/High/Medium/Low/Unknown).
- `trivy image` liệt kê CVE với: ID, package, installed version, fixed version, severity.
- `report.json` và `report.sarif` tạo thành công.

## Tiêu chí hoàn thành

- [ ] Chạy được cả `docker scout` và `trivy`
- [ ] Hiểu các severity: CRITICAL / HIGH / MEDIUM / LOW / UNKNOWN
- [ ] Biết flag `--ignore-unfixed` để giảm noise
- [ ] Đã thử output JSON/SARIF
- [ ] Đối chiếu được trade-off `distroless` / `alpine` / `scratch`

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `docker scout` báo phải login | `docker login` trước; Scout free cho repo public |
| `trivy: command not found` | macOS: `brew install aquasecurity/trivy/trivy`; Linux: xem trivy.dev |
| Trivy DB tải chậm/lỗi | Lần đầu mất 1-2 phút; nếu fail, retry hoặc set `--cache-dir` |
| Báo "vulnerability database not found" | `trivy image --download-db-only` chạy trước |

## Câu hỏi

- Vì sao `python:3.11-slim` đôi khi có CVE mà code mình không gây ra? *(do OS packages: openssl, libssl, glibc... patch ở base image)*
- Strategy giảm CVE — trade-off?
  - **`distroless`**: tối thiểu OS package → ít CVE nhất, nhưng không có shell để debug.
  - **`alpine`**: nhỏ (~5MB), nhưng dùng `musl` thay `glibc` → có thể incompat với 1 số Python wheel binary.
  - **`scratch`**: rỗng hoàn toàn → chỉ hợp với Go static binary, Rust musl.

## Bài kế tiếp

```bash
cp -r ../54-image-scan ../55-buildx-multiarch
cd ../55-buildx-multiarch
```
