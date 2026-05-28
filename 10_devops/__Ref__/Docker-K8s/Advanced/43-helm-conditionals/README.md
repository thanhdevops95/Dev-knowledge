# Bài 43 — Conditionals, Loops & Named Templates

> ⚠️ **File trong `examples/` là Helm template snippet** (có `{{ ... }}`, `range`, `if`...) — **KHÔNG** `kubectl apply -f` trực tiếp. Copy vào `<chart>/templates/` rồi render bằng `helm template`.

## Phần A — If/Else

`templates/ingress.yaml` chỉ render khi `ingress.enabled=true`. Xem `examples/ingress.yaml`.

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
...
{{- end }}
```

## Phần B — Range (loop)

`templates/multi-env.yaml` tạo nhiều ConfigMap từ array `.Values.environments`. Xem `examples/multi-env.yaml`.

`values.yaml` minh hoạ:
```yaml
environments:
  - name: dev
    replicas: 1
    cpu: "100m"
  - name: staging
    replicas: 2
    cpu: "200m"
  - name: prod
    replicas: 5
    cpu: "500m"
```

Loop trên map:
```yaml
metadata:
  labels:
    {{- range $key, $value := .Values.labels }}
    {{ $key }}: {{ $value | quote }}
    {{- end }}
```

## Phần C — Named Templates (`_helpers.tpl`)

`templates/_helpers.tpl` định nghĩa block tái sử dụng:

```yaml
{{- define "myapp.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

Dùng:
```yaml
metadata:
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
```

## Lệnh thủ công

```bash
helm template myapp-advanced . --debug
helm install myapp ./myapp-advanced --dry-run --debug
```

## Bài kế tiếp

```bash
cp -r ../43-helm-conditionals ../44-helm-hooks
cd ../44-helm-hooks
```
