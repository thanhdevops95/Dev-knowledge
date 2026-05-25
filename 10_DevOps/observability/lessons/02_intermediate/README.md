# 📊 Observability — Intermediate cluster

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Intermediate cluster hoàn thành (5/5 bài)

> 🎯 *Từ "có dashboard" → "SRE practice". Build trên Observability basic (5 bài). Cluster intermediate thứ 4 của `10_DevOps/`. Apply 4+ insight từ `__Ref__/` (SRE practices, blameless postmortem, on-call patterns, burn rate alerts). Output: SRE-grade observability với SLO discipline.*

---

## 🚀 Quick start

- **Đã xong basic?** → [00_intermediate-overview](00_intermediate-overview.md).
- **Alert noise 200/day on-call rage?** → [01_promql-deep-and-alerting](01_promql-deep-and-alerting.md).
- **Loki query timeout, AWS bill spike?** → [02_loki-logql-deep](02_loki-logql-deep.md).
- **P99 latency spike không biết tại sao?** → [03_opentelemetry-instrumentation](03_opentelemetry-instrumentation.md).
- **Engineering velocity stuck, on-call burnout?** → [04_sre-practices](04_sre-practices.md).

---

## 📂 Cấu trúc cluster

```
02_intermediate/
├── README.md                              ← (file này)
├── 00_intermediate-overview.md             ← Intro, không hands-on
├── 01_promql-deep-and-alerting.md
├── 02_loki-logql-deep.md
├── 03_opentelemetry-instrumentation.md
└── 04_sre-practices.md
```

---

## 📖 Lessons — Intermediate cluster (5 bài)

| # | Bài | Trọng tâm | Tag | Thời lượng |
|---|---|---|---|---|
| 00 | [Intermediate overview](00_intermediate-overview.md) | Map 4 mảng + tool stack 2026 + 3am incident scenario | MUST-KNOW | ~13p |
| 01 | [PromQL deep + Alerting](01_promql-deep-and-alerting.md) | Functions deep + recording rules + multi-window burn rate + Alertmanager + cardinality + Mimir/Thanos | MUST-KNOW | ~25p |
| 02 | [Loki + LogQL deep](02_loki-logql-deep.md) | LogQL deep + 10 patterns + structured logging + cardinality + Promtail/Vector/Fluent Bit + retention | MUST-KNOW | ~22p |
| 03 | [OpenTelemetry instrumentation](03_opentelemetry-instrumentation.md) | Manual spans + W3C TraceContext propagation + sampling head/tail + Collector pipeline + correlation 3 pillars | MUST-KNOW | ~22p |
| 04 | [SRE practices](04_sre-practices.md) | SLI/SLO/SLA + error budget + burn rate + blameless postmortem (5 whys) + on-call rotation + toil reduction + DORA metrics | MUST-KNOW | ~25p |

→ **Tổng ~107 phút đọc + 8-10h hands-on**. Sau cluster: Observability tier-1 + SRE practice.

---

## 🎯 Sau cluster bạn làm được

- [ ] Viết PromQL advanced (histogram_quantile, predict_linear, recording rules)
- [ ] Setup multi-window burn rate alerts (Google SRE pattern)
- [ ] Configure Alertmanager routing tree + silence + inhibition
- [ ] Cardinality control — Loki/Prometheus efficient
- [ ] Structured JSON logging với trace_id correlation
- [ ] OTel instrument FastAPI end-to-end (auto + manual + context propagation)
- [ ] Tail-based sampling in OTel Collector
- [ ] Define SLO with OpenSLO + Sloth generate alerts
- [ ] Compute error budget + freeze deploy when exhausted
- [ ] Write blameless postmortem with 5 whys
- [ ] Sustainable on-call rotation (4+ team, alert hygiene, runbooks)
- [ ] Apply DORA metrics tracking

---

## 🔗 Liên kết

### Trong workspace
- ↑ [Observability README](../../README.md)
- ↶ [Basic cluster](../01_basic/) — 5 bài foundation
- 🐳 [Docker intermediate](../../../docker/lessons/02_intermediate/)
- ☸️ [Kubernetes intermediate](../../../kubernetes/lessons/02_intermediate/)
- 🔁 [CI/CD intermediate](../../../ci-cd/lessons/02_intermediate/)
- 🏗️ [IaC basic](../../../iac/) — provisions observability stack
- 🧭 [SRE roadmap](../../../../00_Roadmaps/career/sre-engineer_career-roadmap.md)
- 🧭 [DevOps Engineer roadmap](../../../../00_Roadmaps/career/devops-engineer_career-roadmap.md)

### Tài nguyên ngoài 2026 (must-read)
- 📖 [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — bible (free)
- 📖 [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — practical
- 📖 [PromQL cheat sheet](https://promlabs.com/promql-cheat-sheet/)
- 📖 [Loki docs](https://grafana.com/docs/loki/)
- 📖 [OpenTelemetry docs](https://opentelemetry.io/docs/)
- 📖 [Sloth](https://sloth.dev/) — SLO as code
- 📖 [OpenSLO](https://openslo.com/)
- 📖 [Chaos Mesh](https://chaos-mesh.org/)
- 📖 [Honeycomb blog](https://www.honeycomb.io/blog) — observability patterns
- 📖 [Awesome SRE](https://github.com/dastergon/awesome-sre)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Cluster intermediate thứ 4 của `10_DevOps/`. 5 bài hoàn thành: overview + PromQL deep + LogQL deep + OTel instrumentation + SRE practices. Apply 4+ insight từ `__Ref__/` (SRE practices, blameless postmortem template, on-call sustainable rotation, alert saturation patterns, burn rate alerts). Hoàn thành 4/5 DevOps intermediate cluster (Docker + K8s + CI/CD + Obs). Apply rule Blueprint v0.5.2 (no fictional character).
