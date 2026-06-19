# Week 6 Day 3

# Scheduling, Catchup & Backfills

## Goal

Understand how Airflow schedules workflows over time and how it handles historical processing.

By the end of the day:

* Created scheduled DAGs
* Used cron expressions
* Understood `start_date`
* Observed `catchup=True`
* Understood backfills
* Connected Airflow reruns with idempotent pipelines

---

# Airflow Is Time-Oriented

Before today, Airflow felt like:

```plaintext
Run Task A
↓
Run Task B
↓
Run Task C
```

Today the mental model changed to:

```plaintext
Run workflow for a specific date
```

Airflow thinks in terms of:

```plaintext
2026-06-15
2026-06-16
2026-06-17
...
```

rather than simply:

```plaintext
Run now
```

---

# Scheduled DAG

Created:

```python
with DAG(
    dag_id="daily_shipments",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
)
```

Task:

```python
def process_shipments():
    print("Processing daily shipment data")
```

---

# Schedule

Used:

```python
schedule="@daily"
```

Meaning:

```plaintext
Run once per day
```

Airflow automatically creates DAG Runs according to the schedule.

---

# Cron Expressions

Cron format:

```plaintext
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of Week
│ │ │ └──── Month
│ │ └────── Day of Month
│ └──────── Hour
└────────── Minute
```

Examples:

### Daily at 2 AM

```plaintext
0 2 * * *
```

---

### Hourly

```plaintext
0 * * * *
```

---

### Every 15 Minutes

```plaintext
*/15 * * * *
```

---

### Every Monday at 8 AM

```plaintext
0 8 * * 1
```

---

# Why Pipelines Often Run At 2 AM

Instead of:

```plaintext
12:00 AM
```

many production pipelines run later:

```plaintext
2:00 AM
```

Reason:

```plaintext
Upstream systems may still be producing data.
```

Example:

```plaintext
OMS finishes 12:30

Payments finish 1:00

Inventory finishes 1:15

Pipeline starts 2:00
```

to avoid incomplete data.

---

# start_date

Example:

```python
start_date=datetime(2026, 6, 15)
```

Important:

`start_date` is NOT:

```plaintext
When the DAG starts running
```

Instead it means:

```plaintext
Earliest logical date Airflow may schedule
```

---

# Catchup

Created:

```python
catchup=True
```

with:

```python
start_date=datetime(2026, 6, 15)
schedule="@daily"
```

Observed Airflow automatically creating:

```plaintext
2026-06-15
2026-06-16
2026-06-17
2026-06-18
2026-06-19
```

DAG Runs.

This was the most important observation of the day.

---

# catchup=False

Behavior:

```plaintext
Ignore historical dates

Schedule only current/future runs
```

Useful for:

* Learning projects
* Development
* Pipelines that don't need historical recovery

---

# catchup=True

Behavior:

```plaintext
Create missing historical DAG Runs
```

Useful for:

* Production systems
* Recovery scenarios
* Reprocessing historical data

---

# Why Catchup Exists

Imagine:

```plaintext
Pipeline down for 4 days
```

Without catchup:

```plaintext
4 days of data missing
```

With catchup:

```plaintext
Airflow creates DAG Runs
for all missed dates
```

and automatically recovers.

---

# Backfills

Definition:

```plaintext
Reprocessing historical dates
```

Example:

```plaintext
June 17 pipeline failed
```

Code fixed later.

Business requests:

```plaintext
Reprocess June 17
```

This is a backfill.

---

# Why Idempotency Matters

Bad pipeline:

```sql
INSERT INTO silver
```

Run once:

```plaintext
100 rows
```

Run again:

```plaintext
200 rows
```

Duplicates created.

---

Good pipeline:

```sql
MERGE INTO silver
```

Run once:

```plaintext
100 rows
```

Run again:

```plaintext
100 rows
```

Still correct.

---

# Relationship Between Airflow and MERGE

Airflow makes reruns common:

```plaintext
Catchup
Backfill
Recovery
```

Therefore pipelines should be:

```plaintext
Idempotent
```

to avoid duplicate or inconsistent data.

---

# DAG Runs Observed

Key observation:

One DAG can create many DAG Runs.

Example:

```plaintext
daily_shipments
```

generated:

```plaintext
2026-06-15
2026-06-16
2026-06-17
2026-06-18
2026-06-19
```

Each run represents a specific logical date.

---

# Most Important Lesson

Airflow does not think:

```plaintext
Run pipeline now
```

Airflow thinks:

```plaintext
Run pipeline for a specific date
```

This mindset explains:

* Scheduling
* Catchup
* Backfills
* Historical reruns

---

# Key Takeaways

```plaintext
schedule
=
When Airflow should create DAG Runs

start_date
=
Earliest schedulable logical date

catchup=False
=
Ignore historical dates

catchup=True
=
Create historical DAG Runs

backfill
=
Reprocess historical data

idempotency
=
Safe reruns without duplicates
```

---

# Biggest Takeaway

```plaintext
Airflow does not run pipelines.

Airflow runs pipelines for specific dates.
```
