# 🎓 Services & Networking — Expose pods + Load balance

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~16 phút\
> **Prerequisites:** [Pods & Deployments](01_pods-and-deployments.md)

> 🎯 *Master **Service** (4 types: ClusterIP/NodePort/LoadBalancer/ExternalName), **internal DNS**, **Ingress** (Layer 7 HTTP routing + TLS), **cert-manager** (Let's Encrypt auto), **NetworkPolicy** basic, **debug network**. Sau bài này expose app ra Internet đúng cách.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Pod IP ephemeral** + sao cần Service
- [ ] **4 Service types** — chọn cái nào khi nào
- [ ] **Internal DNS** — `svc-name.namespace.svc.cluster.local`
- [ ] **Ingress** + Ingress controller (nginx, traefik)
- [ ] **cert-manager** + Let's Encrypt auto
- [ ] **NetworkPolicy** — restrict pod-to-pod traffic
- [ ] Debug network: `kubectl exec` + `dig` + `curl`
- [ ] Khi nào dùng **Gateway API** (modern replacement)

---

## Tình huống — Bạn không vào được FastAPI

Bạn deploy Deployment 3 replicas bài 01. Pod IP:
```
fastapi-xxx-1   10.244.0.5
fastapi-xxx-2   10.244.0.6
fastapi-xxx-3   10.244.0.7
```

Bạn curl:
```bash
kubectl exec -it some-pod -- curl 10.244.0.5:8000   # ✅ OK
```

→ Pod-to-pod work. Nhưng:
- Pod IP **ephemeral** — pod restart → IP đổi.
- 3 pods → client connect cái nào? Cần **load balance**.
- Từ ngoài cluster — không reach được Pod IP.

Bạn ngơ:
- Sao K8s không có **fixed endpoint** cho group of pods?
- Internal DNS hoạt động thế nào?
- Expose ra Internet — Service vs Ingress?

Senior:
> *"**Service** abstract pod IP → fixed virtual IP. **Ingress** = Layer 7 HTTP router với TLS. Plus **cert-manager** = Let's Encrypt auto-renew."*

→ Bài này dạy networking K8s đầy đủ.

---

## 1️⃣ Service — Stable endpoint cho group of Pods

Pod có IP ephemeral (đổi khi restart). Service tạo **virtual IP stable** + load balance đến nhiều Pod qua `selector`. Đây là cách K8s giải quyết service discovery — Pod đến/đi, Service không đổi:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi
spec:
  selector:
    app: fastapi              # ← Match Pod labels
  ports:
  - port: 80                   # Service port (clients connect)
    targetPort: 8000           # Pod port
  type: ClusterIP              # Default — internal only
```

### Architecture

Khi client gọi Service IP, K8s `kube-proxy` (iptables/IPVS rules) **forward đến 1 pod random** theo selector. Client không biết về pod IP cụ thể — đây là core của K8s service mesh:

```
   Client (other pod)
        │
        ▼
   Service "fastapi" (10.96.0.42)    ← Virtual IP, stable
        │
        ├──► Pod 1 (10.244.0.5:8000)
        ├──► Pod 2 (10.244.0.6:8000)
        └──► Pod 3 (10.244.0.7:8000)
        Round-robin
```

→ Client connect **Service IP**. K8s `kube-proxy` (iptables/IPVS) forward → 1 random pod.

### Verify

Sau khi apply Service, dùng 3 lệnh kiểm tra: `kubectl get svc` (Service hiển thị + ClusterIP), `kubectl get endpoints` (Pod IPs đang match selector), test connectivity từ pod khác:

```bash
kubectl apply -f service.yaml

kubectl get svc
# NAME      TYPE        CLUSTER-IP    PORT(S)
# fastapi   ClusterIP   10.96.0.42    80/TCP

kubectl get endpoints fastapi
# ADDRESSES
# 10.244.0.5:8000,10.244.0.6:8000,10.244.0.7:8000

# Test from another pod
kubectl run -it test --image=busybox --rm -- sh
$ wget -O- http://fastapi:80
# "products": [...]
```

### Pod come/go — Service stable

Đây là **superpower chính** của Service — Pod chết/restart/scale thoải mái, Service IP **không đổi**. Client app dùng Service name như DNS, không cần biết Pod nào đang chạy:

```
Pod 1 (10.244.0.5) crash
   → Pod recreated as 10.244.0.99
   → Service endpoints auto-update
   → Client connect Service IP — unchanged
```

→ **Service IP stable suốt vòng đời**. Pod IP ephemeral OK.

---

## 2️⃣ 4 Service types

### 1. ClusterIP (default) — Internal only

ClusterIP là **type mặc định** — Service chỉ accessible bên trong cluster. Pattern phổ biến nhất cho backend services, databases, internal API. Bỏ qua field `type` mặc định là ClusterIP:

```yaml
spec:
  type: ClusterIP        # Hoặc không set
```

→ IP **chỉ reach được trong cluster**. Other Services/Pods connect, không từ ngoài.

**Use case**: backend service (FastAPI), database, cache.

### 2. NodePort — Expose qua port mỗi node

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080         # Optional — auto-assign in 30000-32767
```

→ Mỗi node mở port 30080 → forward Service. Access: `http://<any-node-ip>:30080`.

**Use case**: dev/test. **KHÔNG production** (random port, không TLS).

### 3. LoadBalancer — Cloud LB

```yaml
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
```

→ Cloud provider (AWS/GCP/Azure) **provision external LB** với public IP, route traffic → Service.

```bash
kubectl get svc fastapi
# NAME    TYPE          CLUSTER-IP    EXTERNAL-IP    PORT(S)
# fastapi LoadBalancer  10.96.0.42    203.0.113.1    80:30080/TCP
```

**Use case**: production expose. Cost: $20-50/mo per LB.

⚠️ **Local cluster (kind/minikube)**: External IP `<pending>` forever. Use port-forward hoặc Ingress + tunnel.

### 4. ExternalName — DNS alias

```yaml
spec:
  type: ExternalName
  externalName: api.external-service.com
```

→ Service name resolve thành external DNS. No proxy, just CNAME.

**Use case**: connect external DB từ in-cluster (giả gọi `db` instead of full URL).

### Compare

| Type | Use case | External access | Cost |
|---|---|---|---|
| **ClusterIP** | Internal services | ❌ | $0 |
| **NodePort** | Dev/test expose | Via node IP + port 30000-32767 | $0 |
| **LoadBalancer** | Production expose | ✅ Public IP | $$ per LB |
| **ExternalName** | DNS alias external | DNS only | $0 |

→ **Production**: usually 1 LoadBalancer cho **Ingress controller**, all backends ClusterIP.

---

## 3️⃣ Internal DNS — Auto service discovery

K8s **CoreDNS** addon — every Service gets DNS name automatically.

```
<service>.<namespace>.svc.cluster.local
```

### Examples

| Service `fastapi` in namespace `production` | DNS |
|---|---|
| Full FQDN | `fastapi.production.svc.cluster.local` |
| Cross-namespace from `default` | `fastapi.production` |
| Same namespace | `fastapi` |
| Service port name `http` | `_http._tcp.fastapi.production` (SRV record) |

### Test

```bash
kubectl run -it test --image=busybox --rm -- sh

$ nslookup fastapi
Server:    10.96.0.10
Name:       fastapi.default.svc.cluster.local
Address:    10.96.0.42

$ wget -O- http://fastapi              # short name
$ wget -O- http://fastapi.default      # cross-namespace
$ wget -O- http://fastapi.production.svc.cluster.local    # FQDN
```

### Common DNS error

```
nslookup fastapi
** server can't find fastapi: NXDOMAIN
```

→ Service không exist, hoặc selector không match Pods. Check `kubectl get svc, ep`.

---

## 4️⃣ Ingress — Layer 7 HTTP routing

LoadBalancer Service = 1 LB per Service. Production app có 5 microservices → 5 LBs = $$$$.

**Ingress** = 1 LB router theo HTTP path/host → multiple Services.

```
Internet → 1 LoadBalancer ($20)
              │
              ▼
        Ingress Controller (nginx pod)
              │
   ┌──────────┼──────────┐
   ▼          ▼           ▼
api.com    web.com   admin.com
  ↓          ↓           ↓
fastapi    react      admin
Service    Service    Service
```

### YAML

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: acmeshop
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - acmeshop.vn
    - api.acmeshop.vn
    secretName: acmeshop-tls
  rules:
  - host: acmeshop.vn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: react-frontend
            port:
              number: 80
  - host: api.acmeshop.vn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fastapi
            port:
              number: 80
```

→ 1 Ingress = 2 hosts, routes to 2 Services.

### Ingress Controller — Cần cài đặt

Ingress object **chỉ là spec**. Cần **controller** (pod) implement nó. Popular:

| Controller | Notes |
|---|---|
| **NGINX** | **Most popular** — community + official |
| **Traefik** | Auto-discovery, dynamic config |
| **HAProxy** | Performance |
| **Caddy** | Auto-HTTPS built-in |
| **AWS LB Controller** | Provisions AWS ALB (cloud-native) |
| **GCP GCLB** | GKE managed |

### Install nginx ingress on kind

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

### Path types

```yaml
paths:
- path: /
  pathType: Prefix           # match prefix
- path: /api/v1
  pathType: Prefix            # /api/v1, /api/v1/foo, ...
- path: /exact
  pathType: Exact             # only /exact
```

### Annotations — Controller-specific

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    cert-manager.io/cluster-issuer: letsencrypt-prod
```

→ Annotations = "escape hatch". Modern alternative = **Gateway API** (standardized, replacing Ingress).

---

## 5️⃣ cert-manager — Let's Encrypt auto

Production cần **HTTPS**. Manual cert renewal pain. **cert-manager** auto-fetch + renew.

### Install

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

kubectl get pods -n cert-manager
```

### Create ClusterIssuer — Let's Encrypt

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: ops@acmeshop.vn
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
    - http01:
        ingress:
          class: nginx
```

### Auto request cert via Ingress annotation

```yaml
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts: [acmeshop.vn]
    secretName: acmeshop-tls      # ← cert-manager auto-create
```

→ Apply Ingress → cert-manager request Let's Encrypt → save cert in Secret `acmeshop-tls` → nginx ingress use → HTTPS active. **0 manual work**.

### Verify

```bash
kubectl get certificate
# NAME           READY   SECRET         AGE
# acmeshop-tls   True    acmeshop-tls   2m

kubectl describe certificate acmeshop-tls
```

→ Auto-renew 30 days before expiry.

---

## 6️⃣ NetworkPolicy — Pod-to-pod firewall

K8s default: **mọi pod connect được nhau**. Production: restrict.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-allow-fastapi
spec:
  podSelector:
    matchLabels:
      app: postgres                  # Apply policy on postgres pods
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: fastapi                # ← Only fastapi pods can connect
    ports:
    - protocol: TCP
      port: 5432
```

→ **Default deny + selective allow** — chỉ pods label `app=fastapi` connect được Postgres port 5432.

### Common patterns

```yaml
# Deny all ingress to a pod
spec:
  podSelector: { matchLabels: { app: secret-service } }
  policyTypes: [Ingress]
  ingress: []        # Empty = deny

# Allow same namespace only
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: production

# Restrict egress to specific external IP
egress:
- to:
  - ipBlock:
      cidr: 203.0.113.0/24
  ports:
  - port: 443
```

### Prerequisites

NetworkPolicy **chỉ work** với CNI support: Calico, Cilium, Weave. **Flannel** default = không support! Check.

---

## 7️⃣ Debug network

### Pod-to-pod connectivity

```bash
# Step 1: Exec into a pod
kubectl exec -it some-pod -- sh

# Step 2: DNS
$ nslookup fastapi
$ nslookup fastapi.default.svc.cluster.local

# Step 3: TCP
$ nc -zv fastapi 80
$ wget -O- http://fastapi/healthz
```

### Service endpoints

```bash
kubectl get svc fastapi
kubectl get endpoints fastapi

# If endpoints empty → selector mismatch pods
kubectl get pods --show-labels
# Compare with svc selector
kubectl describe svc fastapi
```

### Ingress status

```bash
kubectl get ingress
# NAME       CLASS   HOSTS                       ADDRESS         PORTS
# acmeshop   nginx   acmeshop.vn,api.acmeshop.vn 203.0.113.10   80, 443

kubectl describe ingress acmeshop
# Events show cert-manager, controller assignment
```

### Test external access

```bash
# Add /etc/hosts if DNS not setup
sudo sh -c 'echo "203.0.113.10 acmeshop.vn api.acmeshop.vn" >> /etc/hosts'

curl -v https://api.acmeshop.vn/
```

### Common errors

| Error | Likely cause |
|---|---|
| Service endpoints empty | Selector mismatch |
| `connection refused` | Pod not listening on port |
| `connection timeout` | NetworkPolicy block / wrong namespace |
| Ingress 502 | Backend Service not ready / no endpoints |
| Ingress 404 | Path/host mismatch rule |
| Cert pending | DNS not point to Ingress, http01 fail |

---

## 8️⃣ Expose FastAPI + React production

### Architecture

```
Internet (acmeshop.vn)
   │
   ▼ DNS A → LoadBalancer IP
LoadBalancer (cloud, 1 IP)
   │
   ▼
Ingress (nginx-ingress controller)
   │
   ├── acmeshop.vn       ──► react-frontend Service ──► React pods
   └── api.acmeshop.vn    ──► fastapi Service       ──► FastAPI pods
```

### `services.yaml`

```yaml
apiVersion: v1
kind: Service
metadata: { name: fastapi }
spec:
  selector: { app: fastapi }
  ports: [{ port: 80, targetPort: 8000 }]
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata: { name: react-frontend }
spec:
  selector: { app: react-frontend }
  ports: [{ port: 80, targetPort: 80 }]
  type: ClusterIP
```

### `ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: acmeshop
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts: [acmeshop.vn, api.acmeshop.vn]
    secretName: acmeshop-tls
  rules:
  - host: acmeshop.vn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend: { service: { name: react-frontend, port: { number: 80 } } }
  - host: api.acmeshop.vn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend: { service: { name: fastapi, port: { number: 80 } } }
```

### Deploy

```bash
kubectl apply -f services.yaml
kubectl apply -f ingress.yaml

# Wait cert
kubectl get cert acmeshop-tls -w

# Test
curl https://acmeshop.vn         # React app
curl https://api.acmeshop.vn/    # FastAPI
```

→ Production-grade: 1 LB, 2 hosts, HTTPS auto. **Cost ~$25/mo** (LB) instead of 2 LBs.

---

## 9️⃣ Gateway API — Modern replacement

**Gateway API** (stable 2023) = next-gen Ingress. Modular, standardized, multi-protocol.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata: { name: acmeshop-gw }
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    port: 443
    protocol: HTTPS
    tls: { ... }
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: { name: api-route }
spec:
  parentRefs: [{ name: acmeshop-gw }]
  hostnames: [api.acmeshop.vn]
  rules:
  - matches: [{ path: { value: / } }]
    backendRefs: [{ name: fastapi, port: 80 }]
```

### Vs Ingress

| Aspect | Ingress | Gateway API |
|---|---|---|
| Maturity | v1 stable | v1 (Oct 2023) |
| Annotations escape | Lots | Standardized fields |
| Role separation | Mixed | Cluster ops / Dev / Service mesh |
| Multi-protocol | HTTP only | HTTP, TCP, UDP, TLS |
| Status 2026 | Still works, legacy direction | **Recommended new clusters** |

→ Mới migrate sang Gateway API. Existing clusters Ingress vẫn OK.

---

## ⚠️ 5 pitfall hay vướng

1. **Service selector mismatch Pod labels** → endpoints empty → connection refused. Check `kubectl get endpoints svc-name`.
2. **`type: LoadBalancer` trên kind/minikube** → External IP `<pending>` forever. Use port-forward hoặc Ingress.
3. **Quên Ingress controller** → Ingress object exist nhưng không route. Install nginx-ingress trước.
4. **TLS secret name sai** trong Ingress → cert không apply. Confirm `kubectl get secret <name>` exist + type `kubernetes.io/tls`.
5. **NetworkPolicy không work** → CNI không support (Flannel). Calico/Cilium needed.

---

## ✅ Self-check

1. **Pod IP ephemeral** — sao cần Service?
2. 4 Service types + use case mỗi cái?
3. **Internal DNS** format cho Service `fastapi` in namespace `production`?
4. **Ingress** vs **LoadBalancer Service** — khi nào dùng cái nào?
5. **cert-manager** giải quyết vấn đề gì?

<details>
<summary>Gợi ý đáp án</summary>

1. Pod restart/crash → IP đổi. Client connect Pod IP = broken khi Pod chết. **Service** = stable virtual IP + load balance N pods. Pod come/go OK, Service endpoint stable.

2. **ClusterIP** (internal services, default), **NodePort** (dev/test expose via node port 30000-32767), **LoadBalancer** (production external, cloud provision LB), **ExternalName** (DNS alias to external service).

3. `fastapi.production.svc.cluster.local` (FQDN). Short: `fastapi.production` (cross-namespace) hoặc `fastapi` (same namespace).

4. **LoadBalancer Service** = 1 cloud LB per service = $$$ khi nhiều services. **Ingress** = 1 LB router theo HTTP path/host → multiple services. Production: 1 Ingress (1 LB) cho all HTTP services. LoadBalancer Service chỉ cho non-HTTP (DB, gRPC) hoặc khi cần dedicated.

5. **TLS certs**: (a) Manual buy + renewal pain — yearly. (b) Let's Encrypt free but manual ACME challenges. **cert-manager** auto: request, validate (http01/dns01), save in Secret, auto-renew 30 days before expiry. Set up once, forget forever.
</details>

---

## ⚡ Cheatsheet

### Service template

```yaml
apiVersion: v1
kind: Service
metadata: { name: app }
spec:
  selector: { app: app }
  ports: [{ port: 80, targetPort: 8000 }]
  type: ClusterIP   # | NodePort | LoadBalancer | ExternalName
```

### Ingress template

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts: [domain.com]
    secretName: domain-tls
  rules:
  - host: domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend: { service: { name: app, port: { number: 80 } } }
```

### Debug

```bash
kubectl get svc <name>
kubectl get endpoints <name>
kubectl describe svc <name>
kubectl describe ingress <name>
kubectl get ingress -A
kubectl get cert -A          # cert-manager
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

### Internal DNS

```
<svc>.<ns>.svc.cluster.local      Full
<svc>.<ns>                        Cross-namespace
<svc>                             Same namespace
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Service** | Stable virtual IP cho group of Pods |
| **ClusterIP** | Internal-only Service (default) |
| **NodePort** | Expose via port on every node |
| **LoadBalancer** | Cloud LB provisioned |
| **ExternalName** | DNS CNAME to external service |
| **Endpoints** | Pod IPs backing a Service |
| **kube-proxy** | Implements Services (iptables/IPVS) |
| **CoreDNS** | K8s DNS addon |
| **Ingress** | Layer 7 HTTP routing object |
| **Ingress Controller** | Implements Ingress (nginx, traefik, ...) |
| **cert-manager** | Auto-provision TLS certs (Let's Encrypt) |
| **ClusterIssuer** | cert-manager config for CA |
| **NetworkPolicy** | Pod-to-pod firewall rules |
| **CNI** | Container Network Interface — Calico, Cilium |
| **Gateway API** | Modern replacement for Ingress |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Pods & Deployments](01_pods-and-deployments.md)
- → Tiếp: [ConfigMaps & Secrets](03_configmaps-and-secrets.md)
- ↑ Cluster: [kubernetes README](../../README.md)

### Cross-reference
- [HTTPS & TLS](../../../../05_Networking/http-https/lessons/01_basic/04_https-tls.md) — TLS basics
- [DNS](../../../../05_Networking/dns/) — DNS for ingress
- [TCP/IP](../../../../05_Networking/tcp-ip-fundamentals/) — networking foundation

### External
- 📖 [K8s docs — Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- 📖 [K8s docs — Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- 📖 [cert-manager docs](https://cert-manager.io/docs/)
- 📖 [Gateway API docs](https://gateway-api.sigs.k8s.io/)
- 📖 [Calico NetworkPolicy](https://docs.tigera.io/calico/latest/network-policy/)

---

> 🎯 *Sau bài này expose K8s app ra Internet đúng cách. Bài kế tiếp dạy **ConfigMaps + Secrets** — manage config & secrets.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước §1 Service definition + Architecture + Verify + Pod come/go + §2 ClusterIP type.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster K8s basic lesson 3/5. Cover: Service concept + 4 types (ClusterIP/NodePort/LoadBalancer/ExternalName) + service discovery DNS + Ingress vs Service + Pod-to-Pod networking + NetworkPolicy intro.
