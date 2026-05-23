# Bài 42 — Helm Template Functions & Pipelines

> **Mục tiêu:** đi sâu Go template trong Helm.
>
> ⚠️ **File trong `examples/` là Helm template snippet** (có `{{ ... }}`) — **KHÔNG** `kubectl apply -f` trực tiếp được! Phải copy vào `myapp-advanced/templates/` rồi render bằng `helm template` hoặc `helm install`.

## Lệnh thủ công

```bash
# 1. Tạo chart mới
helm create myapp-advanced
cd myapp-advanced

# 2. Sửa các file template để dùng built-in objects & functions
# Xem ví dụ trong examples/ của thư mục bài này
```

## Built-in Objects (Phần A)

Copy `examples/configmap.yaml` vào `myapp-advanced/templates/configmap.yaml`:

Truy cập các trường: `.Release.Name`, `.Release.Namespace`, `.Chart.Name`, `.Chart.Version`, `.Capabilities.KubeVersion`.

## Functions phổ biến (Phần B)

Trong `myapp-advanced/templates/deployment.yaml` thay đoạn metadata bằng version đã helper:

```yaml
metadata:
  name: {{ .Release.Name | lower }}-app
  labels:
    app: {{ .Chart.Name | upper }}
    version: {{ .Chart.Version | replace "." "-" }}
spec:
  replicas: {{ .Values.replicaCount | default 1 }}
```

## Pipelines (Phần C)

```yaml
{{ .Values.message | trim | upper | quote }}
{{ .Values.list | join ", " | quote }}
{{ .Values.password | b64enc | quote }}
{{ .Values.config | toYaml | indent 4 }}
```

## Render thử

```bash
helm template myapp-advanced . --debug
helm install --dry-run --debug myapp ./myapp-advanced
```

## Bài tập

1. Viết template sinh Secret từ `password` trong `values.yaml`, dùng `b64enc`.
2. Dùng `randAlphaNum 16` sinh password nếu chưa set.

> ⚠️ **Bẫy `randAlphaNum`:** viết trực tiếp `{{ randAlphaNum 16 | b64enc }}` sẽ sinh password **MỚI mỗi lần `helm upgrade`** → app đang chạy bị fail auth. Cách đúng: combo **`lookup` + `randAlphaNum`** để giữ giá trị cũ khi Secret đã tồn tại.
>
> ```yaml
> # templates/secret.yaml
> {{- $existing := (lookup "v1" "Secret" .Release.Namespace "myapp-secret") -}}
> {{- $password := "" -}}
> {{- if $existing -}}
>   {{- $password = index $existing.data "DB_PASSWORD" | b64dec -}}
> {{- else -}}
>   {{- $password = .Values.dbPassword | default (randAlphaNum 16) -}}
> {{- end }}
> apiVersion: v1
> kind: Secret
> metadata:
>   name: myapp-secret
> type: Opaque
> data:
>   DB_PASSWORD: {{ $password | b64enc | quote }}
> ```
>
> Install lần đầu sinh random, upgrade các lần sau **đọc lại** secret cũ. Production-grade: đẩy secret ra ngoài Helm bằng External Secrets / Sealed Secrets (Bài 68).

## Bài kế tiếp

```bash
cp -r ../42-helm-functions ../43-helm-conditionals
cd ../43-helm-conditionals
```
