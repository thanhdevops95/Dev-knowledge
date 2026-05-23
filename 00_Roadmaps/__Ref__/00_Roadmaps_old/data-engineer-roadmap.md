# 🗺️ Lộ trình Data Engineer

> `[INTERMEDIATE → ADVANCED]` — Xây dựng pipeline dữ liệu quy mô lớn

---

## Data Engineer là gì?

Data Engineer xây dựng **hạ tầng và pipeline** để thu thập, chuyển đổi, và phục vụ dữ liệu cho Data Analyst và Data Scientist.

```
Data Sources     Pipeline (Data Engineer)     Consumers
(APIs, DBs,  →   ETL/ELT → Data Warehouse →   Analysts
 logs, files)    Streaming → Data Lake        Scientists
                                              Dashboards
```

---

## Khác biệt với Data Scientist

| | Data Engineer | Data Scientist |
|---|---|---|
| **Focus** | Infrastructure, pipelines | Analysis, models |
| **Skills** | SQL, Python, Spark, Cloud | Python, ML, Statistics |
| **Output** | Clean data, pipelines | Insights, models |
| **Tools** | Airflow, dbt, Kafka | Jupyter, scikit-learn |

---

## Giai đoạn 1 — Nền tảng

- [ ] **Python** mạnh → [../02-Languages/python/](../02-Languages/python/)
- [ ] **SQL nâng cao** (Window functions, CTEs, Query optimization) → [../05-Databases/sql/](../05-Databases/sql/)
- [ ] **Linux & Bash scripting** → [../01-Fundamentals/terminal/](../01-Fundamentals/terminal/)
- [ ] **Git** → [../01-Fundamentals/git/](../01-Fundamentals/git/)

---

## Giai đoạn 2 — Databases & Storage

- [ ] **Relational DB** — PostgreSQL nâng cao: Partitioning, Indexing
- [ ] **NoSQL** — MongoDB, Cassandra (columnar)
- [ ] **Data Warehouse** — Snowflake, BigQuery, Redshift
- [ ] **Data Lake** — AWS S3, Azure Data Lake, GCS
- [ ] **File formats** — Parquet, Avro, ORC (so với CSV/JSON)

---

## Giai đoạn 3 — ETL/ELT & Pipeline

- [ ] **ETL concepts** — Extract, Transform, Load
- [ ] **Apache Airflow** — Workflow orchestration
- [ ] **dbt (data build tool)** — Transformation trong SQL
- [ ] **Spark basics** — Xử lý dữ liệu lớn (PySpark)
- [ ] **Data quality** — Great Expectations, Soda

---

## Giai đoạn 4 — Streaming

- [ ] **Apache Kafka** — Message streaming
- [ ] **Apache Flink / Spark Streaming** — Real-time processing
- [ ] **Debezium** — Change Data Capture (CDC)

---

## Giai đoạn 5 — Cloud & MLOps

- [ ] **Cloud platform** — AWS (S3, Glue, EMR, Redshift), GCP (BigQuery, Dataflow)
- [ ] **Infrastructure as Code** — Terraform → [../06-DevOps/iac/](../06-DevOps/iac/)
- [ ] **Docker & Kubernetes** → [../06-DevOps/docker/](../06-DevOps/docker/)
- [ ] **Data Observability** — Monte Carlo, Bigeye

---

## Modern Data Stack

```
Ingestion     →    Storage      →   Transform   →   Serve
Fivetran           Snowflake         dbt             Metabase
Airbyte            BigQuery          Spark           Superset
Kafka              Delta Lake        dbt Cloud       Looker
```

---

## 📦 Project thực hành

| Project | Kỹ năng luyện |
|---|---|
| ETL pipeline đọc API → PostgreSQL | Python, SQL, Airflow |
| Real-time dashboard với Kafka | Streaming, Visualize |
| Data Warehouse trên BigQuery | Cloud, dbt, SQL |
| Recommender system data pipeline | End-to-end |
