# Chuyên sâu — 14 bài: Helm, GitOps, Service Mesh + Advanced Bonus

> **Series:** advanced-practice · [← Kubernetes](../K8s/README.md) · [Mục lục tổng](../README.md)

## Tiên quyết

- Hoàn thành K8s Bài 40-41 (đã dùng Helm cơ bản).
- Cluster còn chạy; ≥4-8 GB RAM trống cho Istio.
- Repo GitHub (Bài 45-47).

## Lộ trình 9 bài

### Helm chuyên sâu

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 42 | [`42-helm-functions/`](42-helm-functions/) | Built-in objects, pipelines |
| 43 | [`43-helm-conditionals/`](43-helm-conditionals/) | If/Else, range, named templates |
| 44 | [`44-helm-hooks/`](44-helm-hooks/) | Dependencies, hooks, multi-env |

### GitOps với ArgoCD

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 45 | [`45-argocd-setup/`](45-argocd-setup/) | Install + Application đầu tiên |
| 46 | [`46-gitops-workflow/`](46-gitops-workflow/) | Update qua Git, self-heal, rollback |
| 47 | [`47-applicationset/`](47-applicationset/) | ApplicationSet, Image Updater |

### Service Mesh với Istio

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 48 | [`48-istio-setup/`](48-istio-setup/) | Cài Istio, sidecar, Gateway |
| 49 | [`49-traffic-management/`](49-traffic-management/) | Canary, A/B, fault injection |
| 50 | [`50-istio-security/`](50-istio-security/) | mTLS, AuthZ, Tracing — **dự án cuối** |

### Advanced Bonus (Bài 65-69)

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 65 | [`65-cert-manager/`](65-cert-manager/) | TLS tự động với cert-manager + Let's Encrypt |
| 66 | [`66-prometheus-stack/`](66-prometheus-stack/) | kube-prometheus-stack, ServiceMonitor, PrometheusRule, Grafana |
| 67 | [`67-velero-backup/`](67-velero-backup/) | Velero backup/restore qua MinIO/S3 |
| 68 | [`68-secrets-mgmt/`](68-secrets-mgmt/) | Sealed Secrets + External Secrets Operator |
| 69 | [`69-operator-crd/`](69-operator-crd/) | CRD + Operator pattern (reconcile loop) |

## ⚠️ Lưu ý

- **Helm chart Bitnami** (Bài 44): version trên hub thay đổi — không bắt buộc khớp patch.
- **ArgoCD CLI macOS** (Bài 45): tải bản `darwin` từ [releases](https://github.com/argoproj/argo-cd/releases), KHÔNG `argocd-linux-amd64`.
- **Istio RAM** (Bài 48-50): `minikube start --memory=6144 --cpus=4` (profile minimal) hoặc `--memory=8192` cho profile demo.
- **Bài 50** là dự án tổng hợp — có thể nộp từng phần (mTLS / tracing / Grafana) nếu thiếu thời gian.
- **Helm `randAlphaNum`** (Bài 42, 68): luôn combo với `lookup` để không sinh password mới mỗi lần `helm upgrade`.
- **Let's Encrypt** (Bài 65): luôn test bằng `letsencrypt-staging` trước, tránh rate limit prod (50 cert/domain/tuần).

→ Bắt đầu: [Bài 42](42-helm-functions/)
