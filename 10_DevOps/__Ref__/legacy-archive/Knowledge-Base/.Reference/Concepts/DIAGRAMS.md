# 🎨 DevOps Architecture Diagrams

> **Sơ đồ kiến trúc DevOps phổ biến**

---

## 1. CI/CD Pipeline

```mermaid
graph LR
    subgraph Development
        A[Developer] -->|Push| B[Git Repository]
    end
    
    subgraph CI Pipeline
        B -->|Trigger| C[Build]
        C --> D[Unit Tests]
        D --> E[Lint/Format]
        E --> F[Build Docker Image]
        F --> G[Push to Registry]
    end
    
    subgraph CD Pipeline
        G -->|Deploy| H[Staging]
        H -->|Tests Pass| I[Production]
    end
    
    subgraph Monitoring
        I --> J[Prometheus]
        J --> K[Grafana]
        I --> L[Logs]
    end
```

---

## 2. Kubernetes Architecture

```mermaid
graph TB
    subgraph Control Plane
        API[API Server]
        ETCD[etcd]
        SCH[Scheduler]
        CM[Controller Manager]
    end
    
    subgraph Worker Node 1
        K1[Kubelet]
        KP1[Kube-proxy]
        P1[Pod A]
        P2[Pod B]
    end
    
    subgraph Worker Node 2
        K2[Kubelet]
        KP2[Kube-proxy]
        P3[Pod C]
        P4[Pod D]
    end
    
    API --> ETCD
    API --> SCH
    API --> CM
    API --> K1
    API --> K2
    K1 --> P1
    K1 --> P2
    K2 --> P3
    K2 --> P4
```

---

## 3. Microservices Architecture

```mermaid
graph TD
    subgraph External
        CLIENT[Client]
        CDN[CDN]
    end
    
    subgraph Edge
        LB[Load Balancer]
        GW[API Gateway]
    end
    
    subgraph Services
        AUTH[Auth Service]
        USER[User Service]
        ORDER[Order Service]
        PRODUCT[Product Service]
        NOTIFY[Notification Service]
    end
    
    subgraph Data Layer
        PG[(PostgreSQL)]
        REDIS[(Redis)]
        MQ[Message Queue]
    end
    
    CLIENT --> CDN
    CDN --> LB
    LB --> GW
    GW --> AUTH
    GW --> USER
    GW --> ORDER
    GW --> PRODUCT
    AUTH --> REDIS
    USER --> PG
    ORDER --> PG
    ORDER --> MQ
    MQ --> NOTIFY
```

---

## 4. Three-Tier Architecture

```mermaid
graph TD
    subgraph Presentation Tier
        WEB1[Web Server 1]
        WEB2[Web Server 2]
    end
    
    subgraph Application Tier
        APP1[App Server 1]
        APP2[App Server 2]
        APP3[App Server 3]
    end
    
    subgraph Data Tier
        DB_PRIMARY[(Primary DB)]
        DB_REPLICA[(Replica DB)]
    end
    
    LB[Load Balancer] --> WEB1
    LB --> WEB2
    WEB1 --> APP_LB[Internal LB]
    WEB2 --> APP_LB
    APP_LB --> APP1
    APP_LB --> APP2
    APP_LB --> APP3
    APP1 --> DB_PRIMARY
    APP2 --> DB_PRIMARY
    APP3 --> DB_PRIMARY
    DB_PRIMARY --> DB_REPLICA
```

---

## 5. GitOps Workflow

```mermaid
graph LR
    DEV[Developer] -->|Push| GIT[Git Repository]
    GIT -->|Webhook| CI[CI Pipeline]
    CI -->|Build & Push| REG[Container Registry]
    CI -->|Update| CONFIG[Config Repo]
    ARGO[ArgoCD] -->|Watch| CONFIG
    ARGO -->|Sync| K8S[Kubernetes]
    K8S -->|Pull| REG
```

---

## 6. Observability Stack

```mermaid
graph TD
    subgraph Applications
        APP1[App 1]
        APP2[App 2]
        APP3[App 3]
    end
    
    subgraph Collection
        PROM[Prometheus]
        LOKI[Loki]
        TEMPO[Tempo]
    end
    
    subgraph Visualization
        GRAFANA[Grafana]
    end
    
    subgraph Alerting
        AM[Alertmanager]
        SLACK[Slack]
        PD[PagerDuty]
    end
    
    APP1 -->|Metrics| PROM
    APP2 -->|Metrics| PROM
    APP3 -->|Metrics| PROM
    APP1 -->|Logs| LOKI
    APP2 -->|Logs| LOKI
    APP3 -->|Logs| LOKI
    APP1 -->|Traces| TEMPO
    APP2 -->|Traces| TEMPO
    APP3 -->|Traces| TEMPO
    PROM --> GRAFANA
    LOKI --> GRAFANA
    TEMPO --> GRAFANA
    PROM --> AM
    AM --> SLACK
    AM --> PD
```

---

## 7. Docker Networking

```mermaid
graph TD
    subgraph Host
        BRIDGE[Docker Bridge Network]
        
        subgraph Container 1
            C1[nginx:80]
        end
        
        subgraph Container 2
            C2[app:5000]
        end
        
        subgraph Container 3
            C3[redis:6379]
        end
        
        C1 -->|frontend| BRIDGE
        C2 -->|backend| BRIDGE
        C3 -->|backend| BRIDGE
    end
    
    HOST_PORT[Host :8080] -->|Port Mapping| C1
    C2 -->|Connect| C3
```

---

## 8. Security Layers

```mermaid
graph TD
    INTERNET[Internet] --> WAF[WAF]
    WAF --> CDN[CDN/DDoS Protection]
    CDN --> LB[Load Balancer]
    LB --> FW[Firewall]
    FW --> K8S[Kubernetes Cluster]
    
    subgraph Kubernetes Security
        NP[Network Policies]
        RBAC[RBAC]
        PSP[Pod Security]
        SECRETS[Secrets Management]
    end
    
    K8S --> NP
    K8S --> RBAC
    K8S --> PSP
    K8S --> SECRETS
```

---

## 9. Deployment Strategies

### Rolling Update

```mermaid
graph LR
    subgraph Before
        V1_1[v1]
        V1_2[v1]
        V1_3[v1]
    end
    
    subgraph Update 1
        V1_A[v1]
        V1_B[v1]
        V2_A[v2]
    end
    
    subgraph Update 2
        V1_C[v1]
        V2_B[v2]
        V2_C[v2]
    end
    
    subgraph After
        V2_D[v2]
        V2_E[v2]
        V2_F[v2]
    end
    
    Before --> Update 1 --> Update 2 --> After
```

### Blue-Green

```mermaid
graph TD
    LB[Load Balancer]
    
    subgraph Blue Environment
        B1[v1]
        B2[v1]
    end
    
    subgraph Green Environment
        G1[v2]
        G2[v2]
    end
    
    LB -->|100%| Blue Environment
    LB -.->|0%| Green Environment
```

### Canary

```mermaid
graph TD
    LB[Load Balancer]
    
    subgraph Stable
        S1[v1]
        S2[v1]
        S3[v1]
        S4[v1]
        S5[v1]
        S6[v1]
        S7[v1]
        S8[v1]
        S9[v1]
    end
    
    subgraph Canary
        C1[v2]
    end
    
    LB -->|90%| Stable
    LB -->|10%| Canary
```

---

## 10. Cloud Infrastructure

```mermaid
graph TB
    subgraph Region
        subgraph AZ-1
            VPC1[VPC]
            SUB1[Public Subnet]
            SUB2[Private Subnet]
            EC2_1[EC2]
            RDS1[(RDS Primary)]
        end
        
        subgraph AZ-2
            SUB3[Public Subnet]
            SUB4[Private Subnet]
            EC2_2[EC2]
            RDS2[(RDS Standby)]
        end
    end
    
    IGW[Internet Gateway] --> VPC1
    IGW --> SUB1
    IGW --> SUB3
    ALB[Application LB] --> EC2_1
    ALB --> EC2_2
    EC2_1 --> RDS1
    EC2_2 --> RDS1
    RDS1 -.->|Replication| RDS2
    S3[(S3 Bucket)]
    EC2_1 --> S3
    EC2_2 --> S3
```

---

## 📖 Cách sử dụng diagrams

1. **Study**: Xem để hiểu kiến trúc
2. **Present**: Dùng trong presentations
3. **Document**: Copy vào documentation
4. **Reference**: Xem khi thiết kế hệ thống

**Mermaid** có thể render trong:

- GitHub Markdown
- GitLab Markdown  
- VS Code (với extension)
- Notion
- Obsidian

---

**💡 Tip**: Tạo diagrams riêng cho project của bạn!
