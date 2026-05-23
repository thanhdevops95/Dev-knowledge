# 📊 Lộ trình Data Engineer

> `[BEGINNER → ADVANCED]`
> **Prerequisite:** [00-overview.md](./00-overview.md)

---

## Tại sao Data Engineering?

Dữ liệu là "dầu mỏ mới" — nhưng dầu thô cần được **khai thác, vận chuyển, lọc và lưu trữ** trước khi sử dụng. Data Engineer xây dựng toàn bộ hệ thống pipeline đó.

### So sánh các vai trò Data

| | Data Engineer | Data Analyst | Data Scientist |
|---|---|---|---|
| **Nhiệm vụ chính** | Xây pipeline, hạ tầng dữ liệu | Phân tích, báo cáo, dashboard | Mô hình ML, dự đoán |
| **Công cụ** | SQL, Spark, Airflow, Kafka | SQL, Excel, Tableau, Power BI | Python, Sklearn, TensorFlow |
| **Ví von** | Xây ống nước | Đọc đồng hồ nước | Phát minh máy lọc nước |
| **Output** | Data pipeline, warehouse | Report, insight | Model, prediction |

---

## Sơ đồ lộ trình

```
SQL ──→ Python for Data ──→ ETL/ELT Concepts
                                  │
          ┌───────────────────────┘
          ▼
   Orchestration ──→ Transformation (dbt)
    (Airflow)              │
          ┌────────────────┘
          ▼
   Big Data (Spark) ──→ Streaming (Kafka)
                              │
          ┌───────────────────┘
          ▼
   Data Warehouse ──→ Data Lake ──→ Data Quality
          │
          ▼
   Cloud Data Platform (BigQuery / Redshift / Synapse)
```

---

## Phase 1 — SQL (Nền tảng cốt lõi)

> 🎯 SQL chiếm ~60% công việc hàng ngày của Data Engineer

- [ ] SELECT, JOIN, GROUP BY, Window Functions
- [ ] Subqueries, CTEs, Recursive queries
- [ ] Indexes, query plans, optimization
- [ ] PostgreSQL hoặc MySQL (chọn 1 làm chính)
- [ ] Data modeling: normalization, star schema, snowflake schema
- 📄 [SQL Basics](../08-Databases/sql/01-sql-basics.md)
- 📄 [PostgreSQL Advanced](../08-Databases/sql/02-postgresql-advanced.md)
- 📄 [Query Optimization](../08-Databases/sql/03-query-optimization-practices.md)
- 📄 [Relational Modeling](../08-Databases/data-modeling/01-relational-modeling-fundamentals.md)
- 📄 [Warehouse Modeling](../08-Databases/data-modeling/03-warehouse-modeling-fundamentals.md)

---

## Phase 2 — Python for Data

- [ ] Python cơ bản: data types, functions, OOP, file I/O
- [ ] NumPy & Pandas: DataFrames, transformations, aggregations
- [ ] Xử lý file: CSV, JSON, Parquet, Avro
- 📄 [Python Basics](../05-Languages/python/01-python-basics.md)
- 📄 [Python Advanced](../05-Languages/python/02-python-advanced.md)
- 📄 [NumPy & Pandas](../14-AI-ML/03-numpy-pandas-basics.md)
- 📄 [Data Formats](../08-Databases/data-formats/01-data-formats-compare.md)

---

## Phase 3 — ETL / ELT Concepts

- [ ] ETL vs ELT: khi nào dùng cái nào?
- [ ] Extract từ APIs, databases, files, streams
- [ ] Transform: cleaning, deduplication, enrichment
- [ ] Load vào warehouse / data lake
- [ ] Batch vs Real-time processing
- 📄 [ETL/ELT Basics](<../15-Data Engineering/etl/01-etl-elt-basics.md>)
- 📄 [Data Engineering Overview](<../15-Data Engineering/01-data-eng-overview.md>)

---

## Phase 4 — Orchestration (Airflow)

> 🎵 "Nhạc trưởng" điều phối các bước trong pipeline

- [ ] Apache Airflow: DAGs, Operators, Sensors
- [ ] Task dependencies, retries, SLAs
- [ ] Scheduling, backfill, data-aware scheduling
- [ ] Prefect (alternative hiện đại hơn)
- 📄 [Airflow Basics](<../15-Data Engineering/orchestration/01-airflow-basics.md>)
- 📄 [Prefect](<../15-Data Engineering/orchestration/02-prefect-basics.md>)

---

## Phase 5 — Transformation (dbt)

- [ ] dbt (data build tool): models, refs, sources
- [ ] Testing trong dbt: schema tests, data tests
- [ ] Documentation & lineage tự động
- [ ] Incremental models, snapshots
- 📄 [dbt Basics](<../15-Data Engineering/transformation/01-dbt-basics.md>)

---

## Phase 6 — Big Data Processing (Spark)

> ⚡ Xử lý dữ liệu ở quy mô hàng tỷ records

- [ ] Apache Spark concepts: RDDs, DataFrames, SparkSQL
- [ ] PySpark: transformations, actions, partitioning
- [ ] Spark optimization: broadcast joins, caching, shuffle
- [ ] Spark trên cloud: EMR, Dataproc, Databricks
- 📄 [Spark & PySpark](<../15-Data Engineering/processing/01-spark-pyspark-basics.md>)

---

## Phase 7 — Streaming (Kafka)

- [ ] Apache Kafka: topics, partitions, consumer groups
- [ ] Event-driven architecture patterns
- [ ] Kafka Connect, Schema Registry
- [ ] Apache Flink (stream processing engine)
- [ ] CDC (Change Data Capture) patterns
- 📄 [Kafka & Streaming](<../15-Data Engineering/streaming/01-kafka-streaming-basics.md>)
- 📄 [Flink](<../15-Data Engineering/streaming/02-flink-basics.md>)

---

## Phase 8 — Storage Layer

- [ ] Data Warehouse: Snowflake, BigQuery, Redshift
- [ ] Data Lake: S3/GCS/ADLS + open table formats
- [ ] Delta Lake, Apache Iceberg, Apache Hudi
- [ ] Lakehouse architecture: kết hợp warehouse + lake
- 📄 [Data Warehouse](<../15-Data Engineering/storage/01-data-warehouse-basics.md>)
- 📄 [Data Lake](<../15-Data Engineering/storage/02-data-lake-basics.md>)

---

## Phase 9 — Data Quality & Governance

- [ ] Data quality dimensions: completeness, accuracy, freshness
- [ ] Great Expectations: validation, checkpoints
- [ ] Data contracts giữa producer và consumer
- [ ] Data catalogs, lineage tracking, metadata management
- 📄 [Great Expectations](<../15-Data Engineering/quality/01-great-expectations-basics.md>)

---

## Phase 10 — Cloud Data Platforms

> ☁️ Chọn 1 ecosystem để chuyên sâu

| Cloud | Warehouse | Streaming | Orchestration | Compute |
|---|---|---|---|---|
| **AWS** | Redshift | Kinesis | MWAA (Airflow) | EMR / Glue |
| **GCP** | BigQuery | Pub/Sub | Cloud Composer | Dataproc |
| **Azure** | Synapse | Event Hubs | Data Factory | HDInsight |

- 📄 [Cloud Overview](../10-Cloud/01-cloud-overview.md)
- 📄 [AWS Data](../10-Cloud/aws/05-aws-data-basics.md)
- 📄 [GCP Data](../10-Cloud/gcp/03-gcp-data-basics.md)
- 📄 [Azure Data](../10-Cloud/azure/05-azure-data-basics.md)

---

## 📦 Project thực hành

| Phase | Project | Độ khó |
|---|---|---|
| SQL | Thiết kế star schema và viết analytical queries cho e-commerce DB | ⭐⭐ |
| ETL | Python script: extract từ REST API → transform → load vào PostgreSQL | ⭐⭐ |
| Airflow | Orchestrate daily ETL pipeline với Airflow DAGs | ⭐⭐⭐ |
| dbt | Transformation layer cho warehouse với tests & docs | ⭐⭐⭐ |
| Spark | Batch processing 1GB+ dataset với PySpark trên Databricks | ⭐⭐⭐ |
| Streaming | Real-time pipeline: Kafka → Flink → PostgreSQL | ⭐⭐⭐⭐ |
| Tổng hợp | End-to-end: API ingestion → Kafka → Spark → Warehouse → dbt → Dashboard | ⭐⭐⭐⭐ |

---

## 📚 Tài nguyên

| Loại | Tên | Ghi chú |
|---|---|---|
| Roadmap | [roadmap.sh/dataengineer](https://roadmap.sh/dataengineer) | Interactive roadmap |
| Sách | *Fundamentals of Data Engineering* — Joe Reis | Best intro book (2022) |
| Sách | *Designing Data-Intensive Applications* — Martin Kleppmann | System design cho data |
| Khóa học | [DataTalksClub DE Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Free, project-based |
| Practice | [SQLZoo](https://sqlzoo.net) / [LeetCode SQL](https://leetcode.com/problemset/database/) | Luyện SQL |
| Newsletter | [Data Engineering Weekly](https://www.dataengineeringweekly.com) | Cập nhật xu hướng |
| Community | [r/dataengineering](https://reddit.com/r/dataengineering) | Reddit community |
