# Data Engineering Overview

> **Tags:** `data-engineering` `etl` `elt` `data-pipeline` `airflow` `spark` `dbt` `kafka`
> **Level:** Intermediate | **Prerequisite:** `sql/01-sql-basics.md` `python/01-python-basics.md`

---

## 1. Data Engineer vs Analyst vs Scientist

```
Data Engineer        → Builds pipelines that move and transform data
                       "Plumbing" — reliably gets data to where it needs to be
                       Skills: SQL, Python, Spark, Airflow, Kafka, cloud infra

Data Analyst         → Queries data to answer business questions
                       Dashboards, reports, ad-hoc analysis
                       Skills: SQL, Excel, Tableau/Looker, basic Python/R

Data Scientist       → Builds statistical/ML models, experiments
                       Predictions, recommendations, experiments
                       Skills: Python/R, ML libraries, statistics, SQL

ML Engineer          → Deploys and maintains ML models in production
                       Model serving, monitoring, retraining pipelines
                       Skills: MLOps, Python, Docker/K8s, feature stores

Analytics Engineer   → Bridge between DE and DA
                       Transforms raw data into clean, modeled tables (dbt)
                       Skills: SQL (advanced), dbt, data modeling, Jinja

Typical data flow:
  Sources → [Data Engineers] → Data Platform → [Analysts/Scientists] → Insights
```

---

## 2. Modern Data Stack

```
Ingestion Layer:
  Fivetran, Airbyte     — managed connectors (APIs, DBs, SaaS)
  Kafka, Kinesis         — real-time streaming ingestion
  Custom Python scripts  — custom sources

Storage Layer:
  Raw/Landing:  S3, GCS, Azure Data Lake (cheap, durable)
  Data Warehouse: Snowflake, BigQuery, Redshift (SQL-queryable)
  Data Lakehouse: Databricks Delta Lake, Apache Iceberg (ACID on data lake)

Transformation Layer:
  dbt             — SQL-based transformations with tests and docs
  Spark/PySpark   — large-scale distributed processing
  Pandas          — smaller datasets (<10GB in memory)

Orchestration Layer:
  Apache Airflow  — workflow scheduler (Python DAGs)
  Prefect         — modern Airflow alternative, Python-native
  Dagster         — asset-centric orchestration
  dbt Cloud       — scheduling for dbt pipelines

Serving Layer:
  BI Tools:       Looker (LookML), Tableau, Power BI, Metabase
  APIs:           FastAPI/Flask serving aggregated results
  Feature Store:  Feast (for ML)

Monitoring:
  Great Expectations, Soda   — data quality
  Monte Carlo, Anomalo        — data observability
  OpenMetadata, Datahub       — data catalog
```

---

## 3. ETL vs ELT

```
ETL (Extract → Transform → Load):
  Classic approach (pre-cloud era)
  Transform data BEFORE loading into warehouse
  Processing happens on dedicated ETL servers
  
  Extract: Pull from source systems
  Transform: Clean, join, aggregate ON ETL SERVER
  Load: Push processed data to target

  + Data quality ensured before warehouse
  - Transformation limited by ETL server resources
  - Schema-on-write (must know schema upfront)
  - Harder to re-process historical data

ELT (Extract → Load → Transform):
  Modern approach (cloud era)
  Load RAW data first, transform inside warehouse/lakehouse
  Warehouse does the heavy computation (BigQuery serverless, Redshift, Spark)
  
  Extract: Pull from source systems
  Load: Push raw data directly to warehouse/data lake
  Transform: SQL/dbt/Spark inside the warehouse

  + Leverage warehouse compute power (scales with data)
  + Re-process any time from raw data (idempotent)
  + Schema-on-read (flexible)
  + Modern tools (dbt) make this elegant
  - Raw data costs more storage
  - Need to manage data quality in transform layer
```

---

## 4. Data Pipeline Patterns

```python
# Simple ETL script (Python)
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class SalesETLPipeline:
    def __init__(self, source_conn, target_conn):
        self.source = source_conn
        self.target = target_conn
    
    def extract(self, date: str) -> pd.DataFrame:
        """Extract sales data for a specific date"""
        log.info(f"Extracting sales for {date}")
        
        query = """
        SELECT 
            s.id,
            s.order_date,
            s.amount,
            s.customer_id,
            p.category,
            p.sku
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE DATE(s.order_date) = %(date)s
        """
        
        df = pd.read_sql(query, self.source, params={'date': date})
        log.info(f"Extracted {len(df)} rows")
        return df
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and enrich the data"""
        # Remove duplicates
        df = df.drop_duplicates(subset=['id'])
        
        # Clean amounts
        df['amount'] = df['amount'].abs()  # Remove negatives
        df = df[df['amount'] > 0]          # Remove zero amounts
        
        # Add derived columns
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['day_of_week'] = df['order_date'].dt.day_name()
        df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
        
        # Aggregate to category level
        summary = df.groupby(['category', 'order_date']).agg(
            total_revenue=('amount', 'sum'),
            order_count=('id', 'count'),
            unique_customers=('customer_id', 'nunique'),
            avg_order_value=('amount', 'mean'),
        ).reset_index()
        
        summary['avg_order_value'] = summary['avg_order_value'].round(2)
        summary['processed_at'] = datetime.utcnow()
        
        log.info(f"Transformed to {len(summary)} category summaries")
        return summary
    
    def load(self, df: pd.DataFrame, table: str):
        """Upsert data to target"""
        log.info(f"Loading {len(df)} rows to {table}")
        
        # Use COPY for bulk insert (much faster than INSERT)
        from io import StringIO
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        
        cursor = self.target.cursor()
        
        # Create temp table
        cursor.execute(f"CREATE TEMP TABLE tmp_{table} (LIKE {table})")
        cursor.copy_from(buffer, f"tmp_{table}", sep=',', columns=df.columns.tolist())
        
        # Upsert from temp table
        cursor.execute(f"""
            INSERT INTO {table}
            SELECT * FROM tmp_{table}
            ON CONFLICT (category, order_date) DO UPDATE SET
                total_revenue = EXCLUDED.total_revenue,
                order_count = EXCLUDED.order_count,
                processed_at = EXCLUDED.processed_at
        """)
        
        self.target.commit()
        log.info("Load complete")
    
    def run(self, date: str):
        raw_data = self.extract(date)
        transformed = self.transform(raw_data)
        self.load(transformed, "category_daily_sales")

# Run for yesterday
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
pipeline = SalesETLPipeline(source_conn, target_conn)
pipeline.run(yesterday)
```

---

## 5. Apache Airflow Basics

```python
# dag/sales_pipeline_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='sales_daily_pipeline',
    default_args=default_args,
    description='Daily sales ETL pipeline',
    schedule_interval='0 6 * * *',   # 6 AM UTC every day
    catchup=False,                    # Don't backfill missed runs
    max_active_runs=1,                # Only 1 run at a time
    tags=['sales', 'daily'],
) as dag:
    
    # Task 1: Extract data from source
    def extract_sales(**context):
        execution_date = context['ds']  # Format: 2024-01-15
        hook = PostgresHook(postgres_conn_id='source_db')
        df = hook.get_pandas_df(f"""
            SELECT * FROM sales WHERE DATE(created_at) = '{execution_date}'
        """)
        
        # XCom: pass small data between tasks
        context['task_instance'].xcom_push(key='row_count', value=len(df))
        
        # Save to staging
        df.to_parquet(f'/tmp/sales_{execution_date}.parquet', index=False)
        return f'Extracted {len(df)} rows'
    
    # Task 2: Transform
    def transform_sales(**context):
        execution_date = context['ds']
        
        df = pd.read_parquet(f'/tmp/sales_{execution_date}.parquet')
        # ... transformations
        df.to_parquet(f'/tmp/sales_transformed_{execution_date}.parquet', index=False)
    
    # Task 3: Load
    def load_to_warehouse(**context):
        execution_date = context['ds']
        df = pd.read_parquet(f'/tmp/sales_transformed_{execution_date}.parquet')
        
        hook = PostgresHook(postgres_conn_id='warehouse_db')
        hook.insert_rows(
            table='fact_sales',
            rows=df.values.tolist(),
            replace=True,
            target_fields=df.columns.tolist(),
        )
    
    # Define tasks
    extract = PythonOperator(
        task_id='extract_sales',
        python_callable=extract_sales,
    )
    
    transform = PythonOperator(
        task_id='transform_sales',
        python_callable=transform_sales,
    )
    
    load = PythonOperator(
        task_id='load_to_warehouse',
        python_callable=load_to_warehouse,
    )
    
    # Run dbt models after loading
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/dbt && dbt run --select tag:sales --target prod',
    )
    
    # Define dependencies (task order)
    extract >> transform >> load >> dbt_run
```

---

## 6. dbt — Data Build Tool

```sql
-- models/staging/stg_orders.sql
-- Stage raw data (light cleaning only)
{{ config(materialized='view') }}

SELECT
    id                                          AS order_id,
    CAST(created_at AS TIMESTAMP)               AS created_at,
    LOWER(status)                               AS status,
    CAST(total_amount AS DECIMAL(12,2))         AS total_amount,
    customer_id,
    COALESCE(currency, 'USD')                   AS currency
FROM {{ source('raw', 'orders') }}
WHERE status IS NOT NULL
  AND created_at IS NOT NULL

-- models/marts/fact_orders.sql
-- Business-level model (joins, aggregations)
{{ config(materialized='table') }}    -- Persist as table (vs view)

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}       -- Ref to staging model
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

final AS (
    SELECT
        o.order_id,
        o.created_at,
        o.total_amount,
        o.status,
        c.customer_name,
        c.customer_email,
        c.country,
        DATE_TRUNC('month', o.created_at)       AS order_month
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
)

SELECT * FROM final
```

```yaml
# models/staging/sources.yml — define source tables
version: 2

sources:
  - name: raw
    database: production
    schema: raw_data
    tables:
      - name: orders
        description: "Raw orders from the transactional database"
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 48, period: hour}
        columns:
          - name: id
            description: "Primary key"
            tests:
              - unique
              - not_null
          - name: status
            tests:
              - accepted_values:
                  values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

# models/marts/schema.yml — test your models
models:
  - name: fact_orders
    description: "Cleaned and enriched orders fact table"
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: total_amount
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100000
```

```bash
# dbt commands
dbt run                          # Run all models
dbt run --select stg_orders      # Run specific model
dbt run --select tag:daily       # Run models with tag
dbt run --select +fact_orders    # Run all upstream deps too

dbt test                         # Run all tests
dbt test --select fact_orders

dbt docs generate                # Generate documentation site
dbt docs serve                   # Launch docs server on localhost:8080

dbt deps                         # Install packages (like npm install)
dbt source freshness             # Check if sources are up to date
dbt snapshot                     # Capture slowly changing dimensions
```

---

## 7. PySpark Basics

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Initialize Spark
spark = SparkSession.builder \
    .appName("SalesProcessing") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .getOrCreate()

# Read data
orders_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .parquet("s3://my-bucket/raw/orders/")

# Transformations (lazy — nothing runs yet!)
result = orders_df \
    .filter(F.col("status") == "completed") \
    .filter(F.col("amount") > 0) \
    .withColumn("order_month", F.date_trunc("month", F.col("created_at"))) \
    .withColumn("revenue_usd", 
        F.when(F.col("currency") == "EUR", F.col("amount") * 1.1)
         .otherwise(F.col("amount"))
    ) \
    .groupBy("order_month", "category") \
    .agg(
        F.sum("revenue_usd").alias("total_revenue"),
        F.count("id").alias("order_count"),
        F.countDistinct("customer_id").alias("unique_customers"),
        F.avg("amount").alias("avg_order_value"),
    ) \
    .orderBy("order_month", "total_revenue", ascending=[True, False])

# Action (triggers actual computation)
result.show(20)
result.count()

# Write to Delta Lake
result.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("order_month") \
    .save("s3://my-bucket/processed/category_monthly_revenue/")

# Broadcast join (small table fitting in memory)
products_df = spark.read.parquet("s3://my-data/products/")  # Small table

# Broadcast products to all workers (avoids shuffle join)
result_with_products = large_orders_df.join(
    F.broadcast(products_df),
    on="product_id",
    how="left",
)

spark.stop()
```

---

## 8. Lambda vs Kappa Architecture

```
Lambda Architecture (2012, Nathan Marz):
  ┌────────────────────────────────────────────────────────┐
  │  Batch Layer (Hadoop/Spark)    Serving Layer           │
  │  Process ALL data              Combines results         │
  │  Recomputes everything         from both layers         │
  │  Result: accurate views        ↑                       │
  │                                Merge                   │
  │  Speed Layer (Kafka+Storm)     ↑                       │
  │  Process recent data only      ↑                       │
  │  Result: low-latency views     ↑                       │
  └────────────────────────────────────────────────────────┘
  
  Problem: TWO codebases (batch + stream) that must produce same results!
  Operationally complex, hard to maintain

Kappa Architecture (2014, Jay Kreps):
  ┌────────────────────────────────────────────────────────┐
  │           Stream Processing Only (Kafka/Flink)         │
  │  Real-time stream → process → store results            │
  │  Reprocessing: replay Kafka topic from beginning       │
  │  Single codebase for all processing                    │
  └────────────────────────────────────────────────────────┘
  
  Simpler: ONE pipeline for both real-time and historical
  Requires: Kafka with long retention, fast stream processor

Modern approach: Data Lakehouse
  Combine lake (cheap storage) with warehouse (SQL interface)
  Delta Lake / Apache Iceberg: ACID transactions on Parquet
  Support both batch queries and incremental processing
```

---

*Tài liệu liên quan: `sql/01-sql-basics.md` | `python/02-python-advanced.md` | `messaging/01-message-queues.md`*
