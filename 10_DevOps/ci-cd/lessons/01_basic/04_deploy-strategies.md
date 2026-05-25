# 🎓 Deploy Strategies — Rolling, Blue-Green, Canary, Feature flags

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [Pipeline Patterns](03_pipeline-patterns.md), [Kubernetes basics](../../../kubernetes/)

> 🎯 *Master 5 deployment strategies: **Recreate**, **Rolling**, **Blue-Green**, **Canary**, **Feature flags**. Each strategy có pros/cons. Plus **rollback** + **smoke tests** + **DB migration** challenges. Sau bài này pick + implement đúng strategy cho team.*

## 🎯 Sau bài này bạn sẽ

- [ ] So sánh 5 deployment strategies trên 5 tiêu chí
- [ ] Implement **rolling update** (K8s default)
- [ ] Implement **blue-green** với Service swap
- [ ] **Canary** với traffic split (5% → 100%)
- [ ] **Feature flags** decouple deploy from release
- [ ] **Rollback** strategy + auto-rollback on metric regression
- [ ] **Smoke tests** sau deploy
- [ ] **DB migration** với deploy (backward compatible)

---

## 1️⃣ 5 Strategies overview

5 chiến lược deploy chính 2026 — mỗi cái trade-off khác nhau giữa downtime, resource, risk, complexity. Quy tắc: production user-facing tuyệt đối tránh Recreate; default Rolling cho 80% case:

| Strategy | Downtime | Resource | Risk | Complexity |
|---|---|---|---|---|
| **Recreate** | ❌ Yes | 1x | High | Simple |
| **Rolling** | ✅ No | 1.25x | Medium | Simple |
| **Blue-Green** | ✅ No | **2x** | Low | Medium |
| **Canary** | ✅ No | 1.1x | **Lowest** | High |
| **Feature flag** | ✅ No (decoupled) | 1x | Low | Medium |

---

## 2️⃣ Recreate — Simple but downtime

Strategy đơn giản nhất: **kill all old, start all new**. Downtime trong khoảng pod restart. Chỉ dùng cho dev/staging hoặc schema migration breaking (DB lock anyway):

```
v1 v1 v1 (kill all)  →  v2 v2 v2
                    ↑ downtime here
```

```yaml
spec:
  strategy:
    type: Recreate
```

→ Stop all v1 → start all v2. Downtime = (time to start v2).

### When OK?

Khi nào pick Recreate dù có downtime? 3 trường hợp cụ thể — KHÔNG bao giờ dùng cho production user-facing:

- ✅ Dev/staging.
- ✅ Schema migration breaking (DB lock anyway).
- ✅ Stateful single-instance (some DBs).
- ❌ **NEVER** for production user-facing.

---

## 3️⃣ Rolling — Default K8s

Strategy default của K8s — **gradual replacement** từng pod 1. Luôn có pod serve traffic → zero downtime. Trade-off: mixed version trong thời gian transition:

```
Initial: v1 v1 v1

Step 1: v1 v1 v1 v2   (add 1 v2)
Step 2: v1 v1 v2       (kill 1 v1)
Step 3: v1 v1 v2 v2
Step 4: v1 v2 v2
Step 5: v1 v2 v2 v2
Step 6: v2 v2 v2
```

→ Gradual replace. Always 3 pods serving traffic. Zero downtime.

### K8s config

`maxSurge` + `maxUnavailable` điều khiển tốc độ rolling. Production safe: `maxSurge: 1, maxUnavailable: 0` — luôn có extra pod, không bao giờ giảm capacity:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1                  # 1 extra Pod during update
      maxUnavailable: 0            # 0 Pod down (safe)
```

| Setting | Effect |
|---|---|
| `maxSurge: 25%` | Default — allow 25% extra Pods |
| `maxUnavailable: 25%` | Default — allow 25% Pods down |
| `maxSurge: 1, maxUnavailable: 0` | **Production safe** — extra Pod, 0 disruption |

### Pros

- ✅ Zero downtime.
- ✅ K8s built-in.
- ✅ Auto rollback if probes fail.

### Cons

- ❌ Mixed versions briefly (v1 + v2 serving concurrent traffic).
- ❌ Can't test v2 fully before exposing all users.
- ❌ Rollback = another rolling update (slow).

### Mixed version pitfall

```
User session A → server v1 → call API on server v2 (new endpoint structure)
                             → return error
```

→ **DB schema + API contract must be backward compatible** trong rolling. Chi tiết §8.

---

## 4️⃣ Blue-Green — Instant switch

```
Blue env (v1)           Green env (v2)
  Pods v1 → LB ──────→ users
                          │ switch
  Pods v1                Pods v2  → LB ──→ users
                          ↑ instant
```

### Approach

1. Deploy v2 to **separate environment** ("green").
2. **Smoke test** v2 without users.
3. **Switch traffic** (update Service selector or DNS).
4. v1 environment **idle** — keep for instant rollback.

### K8s implementation

```yaml
# Blue Deployment
apiVersion: apps/v1
kind: Deployment
metadata: { name: app-blue }
spec:
  template:
    metadata: { labels: { app: myapp, version: blue } }
  ...

---
# Green Deployment
apiVersion: apps/v1
kind: Deployment
metadata: { name: app-green }
spec:
  template:
    metadata: { labels: { app: myapp, version: green } }
  ...

---
# Service — controls active version
apiVersion: v1
kind: Service
metadata: { name: app }
spec:
  selector:
    app: myapp
    version: blue                  # ← Switch this to "green"
```

### Switch

```bash
# Currently blue. Test green internally:
kubectl port-forward deploy/app-green 9000:8000
./smoke-test.sh localhost:9000

# OK → switch
kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}'

# Verify
curl https://app.com/version
# v2

# If trouble, instant rollback:
kubectl patch service app -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Pros

- ✅ **Instant rollback** (1 service patch).
- ✅ Test v2 fully isolated.
- ✅ Zero mixed-version traffic.

### Cons

- ❌ **2x resources** (both envs running).
- ❌ Cost $$$$.
- ❌ DB schema migration tricky (both versions access same DB).
- ❌ Cache invalidation across switch.

### When use?

- High-stakes deploy (payment, banking).
- Need instant rollback.
- DB schema compatible across versions.
- Budget for 2x resources during deploy.

---

## 5️⃣ Canary — Gradual traffic shift

```
Initial: 100% → v1

Step 1:  95% → v1     5% → v2 (canary)
Step 2:  80% → v1     20% → v2
Step 3:  50% / 50%
Step 4:   20% → v1    80% → v2
Step 5:   0%          100% → v2
```

→ Slow ramp. Monitor metrics each step. Rollback if regression.

### Approach 1 — K8s Deployments + ingress weight

```yaml
# Stable Deployment
apiVersion: apps/v1
kind: Deployment
metadata: { name: app-stable }
spec:
  replicas: 9                              # 90% of pods
  ...

# Canary Deployment
apiVersion: apps/v1
kind: Deployment
metadata: { name: app-canary }
spec:
  replicas: 1                              # 10% of pods
  ...

# Service select both via label
apiVersion: v1
kind: Service
metadata: { name: app }
spec:
  selector:
    app: myapp                              # Matches both stable + canary
```

→ K8s round-robin → ~10% canary traffic. Crude but works.

### Approach 2 — Ingress weighted routing

```yaml
# nginx-ingress annotation
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "5"   # 5%
spec:
  rules:
  - host: app.com
    http:
      paths:
      - path: /
        backend:
          service: { name: app-canary }
```

→ 5% traffic → canary. Increase weight gradually.

### Approach 3 — Service mesh (Istio, Linkerd)

```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata: { name: app }
spec:
  hosts: [app.com]
  http:
  - route:
    - destination: { host: app, subset: v1 }
      weight: 95
    - destination: { host: app, subset: v2 }
      weight: 5
```

→ Fine-grained: route by header, user ID, geography.

### Approach 4 — Argo Rollouts (K8s-native canary)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata: { name: app }
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: { duration: 10m }            # Auto-monitor
      - setWeight: 25
      - pause: { duration: 10m }
      - setWeight: 50
      - pause: { duration: 10m }
      - setWeight: 100
      analysis:
        templates:
        - templateName: success-rate
        args:
        - name: service-name
          value: app
```

→ Argo Rollouts auto-pause, auto-analyze (Prometheus metrics), auto-rollback if SLO breach. **Best K8s canary tool**.

### Pros

- ✅ **Lowest risk** — bug affect only 5%.
- ✅ Test prod traffic real.
- ✅ Roll back early.

### Cons

- ❌ Setup complex.
- ❌ Need observability (metrics, alerts).
- ❌ Mixed version longer time.

### When use?

- Large user base, can't afford bug for all.
- Have observability + alerting.
- Critical services (payment, auth).

---

## 6️⃣ Feature flags — Decouple deploy from release

```
Deploy code (v2 with feature X behind flag, default OFF)
   ↓
Feature X invisible to users (flag OFF)
   ↓
Enable feature X for 10% users (flag ON for 10%)
   ↓ monitor
Enable for 50%
   ↓
Enable for 100%
   ↓
Remove feature flag in next code release (cleanup)
```

→ **Deploy code != release feature**. Code ship safely (small PRs, fast deploy), feature toggle independently.

### Tools

| Tool | Type | Notes |
|---|---|---|
| **LaunchDarkly** | SaaS | $$$ enterprise, popular |
| **Unleash** | OSS self-host | Free, K8s-friendly |
| **Flagsmith** | Both | OSS + SaaS |
| **PostHog** | OSS | Analytics + flags combined |
| **Split.io** | SaaS | A/B testing focus |
| **OpenFeature** | Standard | SDK abstraction |

### Code example

```python
# FastAPI with Unleash
from UnleashClient import UnleashClient

client = UnleashClient(
    url="http://unleash.local/api",
    app_name="myapp",
    custom_headers={"Authorization": "..."}
)

@app.get("/products")
async def get_products(user: User = Depends(get_user)):
    products = db.products.all()

    if client.is_enabled("new_recommendation_engine", context={"userId": user.id}):
        return await new_recommend_engine(products, user)
    return await old_engine(products, user)
```

→ Old engine 90% users, new 10%. Toggle in Unleash dashboard.

### Pros

- ✅ Deploy daily, release weekly.
- ✅ Kill switch — disable broken feature instantly.
- ✅ A/B test.
- ✅ Targeted release (beta users only).

### Cons

- ❌ Code complexity (`if flag` branching).
- ❌ Flag cleanup debt — old flags pile up.
- ❌ Need infra (vendor or self-host).

→ **2026 standard**: most prod team use feature flags.

---

## 7️⃣ Rollback strategy

### Manual rollback

```bash
# K8s
kubectl rollout undo deployment/app

# Git revert
git revert <bad-commit>
git push                                # Triggers new deploy

# Argo Rollouts
kubectl argo rollouts undo app
```

### Auto-rollback (Argo Rollouts)

```yaml
spec:
  strategy:
    canary:
      analysis:
        templates: [{ templateName: error-rate }]
        args:
        - name: error-threshold
          value: "5"                     # 5% error rate
      # If analysis fail → auto rollback
```

→ Pipeline check Prometheus → error rate > 5% → auto-rollback to previous.

### Database migration constraint

→ **Forward-only DB migrations** (no down migrations easily).

→ Code rollback to v1, but DB schema is v2. Code v1 expect old schema → bug.

**Solution**: **expand-contract pattern**:

```
Migration v1 → v2:
  1. Expand: Add new column (nullable), keep old column
  2. Deploy app v2 (writes both old + new column, reads new)
  3. Backfill old data → new column
  4. Wait deploy stable
  5. Contract: drop old column

Rollback safe at step 1, 2, 3.
After step 5, can't rollback to v1 (old column gone).
```

→ Backward-compatible migrations enable rollback. Critical for rolling/canary.

---

## 8️⃣ Smoke tests

After deploy, **automated checks** verify basic functionality:

```yaml
deploy-prod:
  steps:
  - run: ./deploy.sh
  - name: Smoke tests
    run: |
      sleep 30                              # Wait pods ready
      curl -f https://api.acmeshop.vn/health     # Status 200
      curl -f https://api.acmeshop.vn/products    # Returns products
      curl -f -X POST https://api.acmeshop.vn/test-order
      kubectl logs -l app=fastapi -n production --since=1m | grep -i error || true
  - if: failure()
    run: ./rollback.sh
```

→ Check critical paths post-deploy. Failure → auto rollback.

### Production probes

K8s **readiness probe** = automatic smoke test:

```yaml
readinessProbe:
  httpGet: { path: /ready, port: 8000 }
  initialDelaySeconds: 5
  periodSeconds: 5
```

→ Pod not ready → not added to Service. Deploy continues until enough ready.

### Synthetic monitoring

Tools like **Pingdom**, **Datadog Synthetics**, **Uptime Kuma**: every minute check from multiple regions.

→ Production downtime detected in <1 min.

---

## 9️⃣ Deploy strategy decision của bạn

### Setup của bạn

- 3 environments: dev, staging, production.
- FastAPI + Postgres + React.
- 10K daily users.
- 1-2 deploys per day.

### Strategy choice

| Env | Strategy | Why |
|---|---|---|
| **dev** | Recreate | Cheap, downtime OK |
| **staging** | Rolling | Simulate prod |
| **production** | **Rolling** + **Feature Flags** | Default safe, plus targeted release |

→ Don't need blue-green/canary for 10K users + 1-2 deploys/day. Move complex when scale demands.

### Future scale (1M users)

- production → **Canary với Argo Rollouts** + Prometheus.
- DB migration → expand-contract strict.
- Feature flags critical.

---

## 1️⃣0️⃣ Full deploy pipeline example

```yaml
deploy:
  needs: [build-image]
  runs-on: ubuntu-latest
  environment: production
  steps:
  - uses: actions/checkout@v4

  # 1. Pre-deploy
  - name: Notify Slack start
    run: ./scripts/slack.sh "Deploying ${GITHUB_SHA} to production"

  # 2. DB migration (forward-only, backward-compatible)
  - name: Apply migrations
    run: |
      kubectl run migrate --image=ghcr.io/acmeshop/fastapi:${GITHUB_SHA} \
        --rm -it --restart=Never \
        --command -- alembic upgrade head

  # 3. Deploy (rolling)
  - name: Rolling update
    run: |
      kubectl set image deployment/fastapi \
        fastapi=ghcr.io/acmeshop/fastapi:${GITHUB_SHA} \
        -n production
      kubectl rollout status deployment/fastapi -n production --timeout=10m

  # 4. Smoke tests
  - name: Smoke tests
    run: |
      sleep 30
      curl -f https://api.acmeshop.vn/health
      curl -f https://api.acmeshop.vn/products
      curl -f -X POST https://api.acmeshop.vn/test-checkout

  # 5. Check error rate
  - name: Verify error rate
    run: |
      ERR=$(curl -s "https://prometheus/api/v1/query?query=rate(http_errors_total[5m])" | jq '.data.result[0].value[1]')
      if (( $(echo "$ERR > 0.05" | bc -l) )); then
        echo "Error rate ${ERR} > 5% — rolling back"
        kubectl rollout undo deployment/fastapi -n production
        exit 1
      fi

  # 6. Post-deploy
  - name: Notify Slack success
    if: success()
    run: ./scripts/slack.sh "✅ Deployed successfully"

  - name: Notify Slack failure + rollback
    if: failure()
    run: |
      ./scripts/slack.sh "🚨 Deploy failed, rolling back"
      kubectl rollout undo deployment/fastapi -n production
```

→ Production-grade: migration → rolling → smoke test → metric check → auto rollback. Slack notify both success/fail.

---

## ⚠️ 5 pitfall hay vướng

1. **Recreate prod** → downtime. Use rolling.
2. **Rolling với DB schema breaking** → mixed version error. Expand-contract migration.
3. **Blue-green chia DB** → 2 versions write same DB. DB must be backward compat anyway.
4. **Canary without metrics** → blind ramp. Setup Prometheus + alerts first.
5. **No smoke test** → bad deploy users discover first. Always smoke + auto-rollback.

---

## ✅ Self-check

1. 5 strategies — pick cho **payment service** + **dev environment**?
2. **Rolling update** issue gì với DB schema breaking?
3. **Blue-green** — 2x resources nhưng giải quyết vấn đề gì?
4. **Canary 5%** + Prometheus auto-rollback — flow?
5. **Feature flag** decouple gì với deployment?

<details>
<summary>Gợi ý đáp án</summary>

1. **Payment** = critical → **Canary** với Argo Rollouts + Prometheus auto-rollback (lowest risk) hoặc **Blue-Green** (instant rollback). **Dev** → **Recreate** (cheap, downtime fine).

2. **Mixed version** during rollout. App v1 + v2 traffic concurrent → v1 sees v2's schema (or vice versa) → errors. Fix: **expand-contract migration**. Add new column nullable first, deploy code v2 (writes both columns), backfill, then drop old column in later release. Backward compat throughout.

3. **2x resources** = both envs run concurrently. Solves: (a) **instant rollback** (1 service patch). (b) **Test v2 fully** isolated before exposing users. (c) **Zero mixed-version traffic** — clean switch.

4. (1) Deploy v2 to 5% pods (canary). (2) Argo Rollouts auto-query Prometheus every X min (`error_rate{version=v2}`). (3) If error_rate > threshold → auto-rollback. (4) Else → wait pause duration → ramp to 25%, 50%, 100%. Each step gated by metrics.

5. **Code deployment** vs **feature release**. Deploy code anytime (feature behind flag OFF). Release feature anytime (flag ON for 10%, then 50%, then 100%). Decouple risk: bad code = rollback deploy. Bad feature = toggle flag off (instant). Plus A/B test.
</details>

---

## ⚡ Cheatsheet

### Strategy choice

```
Recreate     → dev, staging (downtime OK)
Rolling      → most production (default)
Blue-Green    → critical + instant rollback
Canary        → critical + observability
Feature Flag  → decouple deploy from release
```

### K8s rolling

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Argo Rollouts canary

```yaml
strategy:
  canary:
    steps:
    - setWeight: 5
    - pause: { duration: 10m }
    - setWeight: 25
    - pause: { duration: 10m }
    - setWeight: 100
    analysis:
      templates: [{ templateName: success-rate }]
```

### Rollback

```bash
kubectl rollout undo deployment/app
git revert HEAD                # → triggers redeploy
kubectl argo rollouts undo app
```

### Smoke test

```yaml
- curl -f https://api/health
- curl -f https://api/critical-endpoint
- check error rate Prometheus
- on fail → rollback
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Recreate** | Stop all → start all (downtime) |
| **Rolling update** | Gradual replace, default K8s |
| **Blue-Green** | 2 envs, instant switch |
| **Canary** | Gradual traffic ramp 5% → 100% |
| **Feature flag** | Toggle feature without redeploy |
| **`maxSurge` / `maxUnavailable`** | Rolling update params |
| **Argo Rollouts** | K8s controller for canary/blue-green |
| **Service mesh** | Istio/Linkerd for traffic management |
| **Expand-contract** | DB migration pattern for safe rollback |
| **Smoke test** | Quick automated check post-deploy |
| **Auto-rollback** | Pipeline rollback on metric regression |
| **Synthetic monitoring** | Periodic prod check from multiple regions |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Pipeline Patterns](03_pipeline-patterns.md)
- ↑ Cluster: [ci-cd README](../../README.md)

### Cross-reference
- [K8s Pods & Deployments](../../../kubernetes/lessons/01_basic/01_pods-and-deployments.md) — rolling update K8s
- [Postgres migrations](../../../../06_Databases/postgresql/lessons/01_basic/04_backup-and-replication.md)

### External
- 📖 [Argo Rollouts docs](https://argoproj.github.io/argo-rollouts/)
- 📖 [Unleash](https://www.getunleash.io/) — OSS feature flags
- 📖 [LaunchDarkly](https://launchdarkly.com/)
- 📖 [Martin Fowler: Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- 📖 [Martin Fowler: Canary Release](https://martinfowler.com/bliki/CanaryRelease.html)
- 📖 [Feature Toggles — Pete Hodgson](https://martinfowler.com/articles/feature-toggles.html)

---

> 🎯 *Cluster CI/CD basic 5/5 đóng. Bạn pick + implement deploy strategy phù hợp. Bài kế tiếp ngoài cluster: GitOps (ArgoCD), Helm, advanced patterns.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước §1 5 Strategies + §2 Recreate + When OK + §3 Rolling + K8s config.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster ci-cd basic lesson 5/5. Cover: 5 strategies (Recreate/Rolling/Blue-Green/Canary/Feature Flags) + decision matrix + K8s implementation + DB migration backward compat + rollback patterns.
