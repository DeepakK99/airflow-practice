# Week 6 Day 5

# Bronze → Silver → Gold Pipeline Orchestration

## Goal

Build a realistic Airflow DAG that resembles a real Data Engineering workflow.

By the end of today:

* Built a medallion architecture DAG
* Used sequential dependencies
* Used parallel execution
* Implemented data quality gates
* Understood Airflow as a control plane
* Connected orchestration to real-world DE platforms

---

# Key Mindset Shift

Before:

```plaintext
Task A
↓
Task B
↓
Task C
```

Today:

```plaintext
Data Platform Workflow
```

The DAG no longer represents arbitrary tasks.

It represents movement and transformation of data through a platform.

---

# Medallion Pipeline V1

Created:

```plaintext
Extract Shipments
        ↓

Bronze Validation
        ↓

Build Silver
        ↓

Silver Quality Check
        ↓

Build Gold
        ↓

Generate Metrics
```

---

# Task Classification

## Data Processing Tasks

```plaintext
extract_shipments

build_silver

build_gold

generate_metrics
```

Purpose:

```plaintext
Move
Transform
Enrich
Aggregate
```

data.

---

## Data Quality Tasks

```plaintext
validate_bronze

silver_quality_check
```

Purpose:

```plaintext
Verify data correctness
```

Examples:

```plaintext
Schema validation

Null checks

Duplicate checks

Range checks

Freshness checks
```

---

# Processing vs Validation

A mature pipeline often follows:

```plaintext
Process
↓
Validate
↓
Process
↓
Validate
↓
Process
```

rather than:

```plaintext
Process everything
↓
Hope it works
```

---

# Medallion Pipeline V2

Introduced multiple data sources.

Architecture:

```plaintext
start

      ↓

extract_customer
extract_shipment

      ↓

build_silver

      ↓

quality_check

      ↓

build_gold

      ↓

generate_metrics

      ↓

end
```

---

# Parallel Execution

Implemented:

```plaintext
extract_customer

extract_shipment
```

in parallel.

Reason:

```plaintext
No dependency exists between them
```

Therefore:

```plaintext
Both can run simultaneously
```

---

# Runtime Benefit

Example:

```plaintext
Customer Extract = 5 min

Shipment Extract = 10 min
```

Sequential:

```plaintext
5 + 10 = 15 min
```

Parallel:

```plaintext
max(5,10) = 10 min
```

Large runtime savings.

---

# Fan-In Pattern

Observed:

```plaintext
extract_customer
        ↘

         build_silver

        ↗
extract_shipment
```

Meaning:

```plaintext
build_silver
```

waits for:

```plaintext
ALL upstream tasks
```

to succeed.

---

# EmptyOperator

Added:

```plaintext
start

end
```

nodes.

Purpose:

```plaintext
Improve readability
```

Benefits:

* Clear workflow boundaries
* Easier visualization
* Better organization for large DAGs

---

# Data Quality Gate

Modified:

```python
def silver_quality_check():
    raise Exception("Data quality failure")
```

Observed:

```plaintext
quality_check
❌

build_gold
⛔ upstream_failed

generate_metrics
⛔ upstream_failed

end
⛔ upstream_failed
```

---

# Why This Is Desirable

Bad data should never reach:

```plaintext
Gold
Metrics
Dashboards
```

Examples:

```plaintext
Negative revenue

Missing shipment IDs

Unexpected row counts
```

A failed quality check should stop the pipeline.

---

# Data Quality Gate Pattern

```plaintext
Build Silver
      ↓

Quality Check
      ↓

Build Gold
```

Only trusted data proceeds downstream.

---

# Real Production Pattern

```plaintext
Bronze
   ↓

Bronze Validation
   ↓

Silver
   ↓

Silver Quality Check
   ↓

Gold
   ↓

Gold Quality Check
   ↓

Dashboard
```

Multiple quality gates are common.

---

# Airflow As A Control Plane

Important realization:

Airflow did not actually:

```plaintext
Transform data

Build Silver

Build Gold
```

Our tasks only executed:

```python
print(...)
```

yet Airflow orchestrated the workflow.

---

# Control Plane vs Data Plane

Airflow:

```plaintext
Coordinates
Schedules
Monitors
Retries
Orchestrates
```

---

Spark / Databricks / Python:

```plaintext
Read data
Transform data
Write data
```

---

Mental model:

```plaintext
Airflow
=
Traffic Controller

Spark
=
Worker
```

---

# How Spark Fits Into Airflow

Airflow does not execute Spark directly.

Typical flow:

```plaintext
Airflow
↓
Submit Spark Job
↓
Spark Cluster Executes
↓
Airflow Waits
```

---

# Common Integration Approaches

## PythonOperator

```plaintext
Airflow
↓
Python Function
↓
Local PySpark Script
```

Simple learning setup.

---

## SparkSubmitOperator

```plaintext
Airflow
↓
spark-submit
↓
Spark Cluster
```

Traditional production approach.

---

## Databricks Operator

```plaintext
Airflow
↓
Databricks API
↓
Databricks Job
↓
Databricks Cluster
```

Common in modern organizations.

---

# Airflow Connections

Airflow stores connection information separately.

Examples:

```plaintext
spark_default

aws_default

databricks_default
```

Stored in:

```plaintext
Admin
↓
Connections
```

DAGs reference:

```python
conn_id="spark_default"
```

instead of hardcoding credentials.

---

# Brewery Platform DAG Design

Final architecture:

```plaintext
start

   ↓

[extract_shipment,
 extract_customer,
 extract_inventory]

   ↓

[validate_shipment,
 validate_customer,
 validate_inventory]

   ↓

build_silver

   ↓

validate_silver

   ↓

build_gold

   ↓

validate_gold

   ↓

generate_metrics

   ↓

validate_metrics

   ↓

refresh_dashboard

   ↓

end
```

---

# Why This Design Works

Parallel extraction:

```plaintext
Lower runtime
```

---

Source-level validation:

```plaintext
Catch issues early
```

---

Silver validation:

```plaintext
Ensure trusted curated data
```

---

Gold validation:

```plaintext
Protect business metrics
```

---

Metrics validation:

```plaintext
Protect dashboards
```

---

# Key Takeaways

```plaintext
Parallel Tasks
=
Independent work

Fan-In
=
Wait for all upstream tasks

Quality Gate
=
Block bad data

Airflow
=
Control Plane

Spark/Databricks
=
Data Plane

Connections
=
How Airflow reaches external systems
```

---

# Biggest Lesson

```plaintext
Airflow is not a data processing engine.

Airflow is an orchestration engine that coordinates the movement of data through a platform.
```

---

# Interview Takeaway

If asked:

> How would you orchestrate a medallion architecture?

A strong answer is:

```plaintext
Bronze
↓
Validation
↓
Silver
↓
Quality Checks
↓
Gold
↓
Metrics
↓
Dashboard
```

with:

```plaintext
Airflow orchestration

Retries

Monitoring

Alerts

Data quality gates
```

to ensure reliable and trustworthy data delivery.
