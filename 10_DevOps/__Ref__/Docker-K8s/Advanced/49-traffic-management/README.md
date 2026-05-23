# Bài 49 — Traffic Management (Canary, A/B, Fault Injection)

## Phần A — Canary 90/10

```bash
kubectl apply -f deploys-v1-v2.yaml      # 2 Deployment label version
kubectl apply -f destination-rule.yaml   # subset v1/v2
kubectl apply -f virtualservice-canary.yaml  # 90% v1, 10% v2

# Test
for i in {1..100}; do
  curl -s http://myapp.local/config | grep version
done | sort | uniq -c
# ~90 lần v6.0 (v1), ~10 lần v7.0/v8.0 (v2)
```

Tăng dần: 50/50 rồi 0/100 bằng sửa `weight` trong `virtualservice-canary.yaml` và `kubectl apply` lại.

## Phần B — A/B Testing theo header

```bash
kubectl apply -f virtualservice-ab.yaml

# User thường → v1
curl http://myapp.local

# Beta tester → v2
curl -H "user-type: beta-tester" http://myapp.local
```

## Phần C — Fault Injection

```bash
kubectl apply -f virtualservice-fault.yaml
# 50% request bị delay 5s
# 10% request bị abort 500
```

## Bài kế tiếp

```bash
cp -r ../49-traffic-management ../50-istio-security
cd ../50-istio-security
```
