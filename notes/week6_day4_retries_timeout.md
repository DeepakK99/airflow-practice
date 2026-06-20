# Week 6 Day 4

# Retries, Failures & Operational Resilience

## Goal

Learn how Airflow handles failures and how production pipelines remain resilient.

By the end of today:

* Configured retries
* Configured retry delays
* Observed task retries
* Configured execution timeouts
* Observed timeout failures
* Understood failure propagation
* Developed operational thinking

---

# Key Mindset Shift

A production pipeline is not one that never fails.

A production pipeline is one that:

```plaintext
Fails safely
Recovers automatically when possible
Alerts when human intervention is required
```

---

# Retries

Created:

```python
task = PythonOperator(
    task_id="flaky_task",
    python_callable=flaky_task,
    retries=2,
    retry_delay=timedelta(seconds=20)
)
```

Observed task lifecycle:

```plaintext
running
↓
up_for_retry
↓
running
↓
up_for_retry
↓
running
↓
failed
```

---

# Important Discovery

The original retry example used:

```python
attempt_counter = {"count": 0}
```

Expected:

```plaintext
Attempt 1
Attempt 2
Attempt 3
```

Observed:

```plaintext
Attempt 1
Attempt 1
Attempt 1
```

Reason:

Each retry is a completely new task execution.

Airflow does not preserve Python process memory between retries.

---

# Practical Lesson

Do not rely on:

```python
global variables
```

for persistent state.

Use:

```plaintext
Database
S3
Files
APIs
Metadata stores
```

for durable state.

---

# Why Retries Exist

Retries help with:

```plaintext
Temporary API outages
Database connection issues
Network hiccups
Transient infrastructure failures
```

Example:

```plaintext
API returns 503
↓
Wait
↓
Retry
↓
Success
```

Without retries:

```plaintext
Pipeline fails unnecessarily
```

---

# Retry Delay

Example:

```python
retry_delay=timedelta(seconds=20)
```

Purpose:

```plaintext
Give external systems time to recover
```

Bad:

```plaintext
Fail
Retry immediately
Fail
Retry immediately
Fail
```

Good:

```plaintext
Fail
Wait
Retry
```

---

# When Retries Should Be Used

Good candidates:

```plaintext
Temporary database outage
Temporary API outage
Network timeout
S3 throttling
```

These are transient failures.

---

# When Retries Should NOT Be Used

Example:

```plaintext
Column does not exist
Wrong schema
Bad SQL syntax
Incorrect configuration
```

These are deterministic failures.

Retrying produces:

```plaintext
Same input
Same code
Same failure
```

No benefit.

---

# Example

Error:

```plaintext
Column shipment_cost does not exist
```

Recommended:

```python
retries=0
```

Reason:

A human must fix the issue.

Retries only delay alerting.

---

# Execution Timeouts

Created:

```python
execution_timeout=timedelta(seconds=10)
```

Task:

```python
time.sleep(30)
```

Observed:

```plaintext
running
↓
failed
```

Logs contained:

```plaintext
AirflowTaskTimeout
```

---

# Why Timeouts Exist

Normal runtime:

```plaintext
2 minutes
```

Unexpected runtime:

```plaintext
45 minutes
```

Potential causes:

```plaintext
Infinite loop
Database deadlock
Hung API call
Poor query plan
```

Without timeout:

```plaintext
Task runs indefinitely
Resources wasted
SLA missed
```

With timeout:

```plaintext
Task killed
Marked failed
Alert generated
```

---

# Retries vs Timeouts

Retries:

```plaintext
Task failed too quickly
```

Examples:

```plaintext
503
Connection error
Temporary outage
```

---

Timeouts:

```plaintext
Task never finished
```

Examples:

```plaintext
Infinite loop
Hung API call
Query stuck
```

---

# Failure Propagation

DAG:

```plaintext
extract
↓
validate
↓
load
```

Forced:

```plaintext
validate
```

to fail.

Observed:

```plaintext
extract
✅

validate
❌

load
⛔ upstream_failed
```

---

# Why Failure Propagation Is Good

Imagine:

```plaintext
Read Bronze
↓
Validate
↓
Build Silver
↓
Build Gold
↓
Refresh Dashboard
```

If validation fails:

```plaintext
Silver should not run
Gold should not run
Dashboard should not refresh
```

Airflow protects downstream systems automatically.

---

# Trigger Rule

Default trigger rule:

```plaintext
all_success
```

Meaning:

```plaintext
Run only when all upstream tasks succeed
```

This is why:

```plaintext
load
```

did not execute.

---

# Production Example

Pipeline:

```plaintext
Bronze
↓
Silver
↓
Gold
↓
Dashboard
```

Silver fails.

Desired behavior:

```plaintext
Stop downstream tasks
Send alert
Investigate issue
Backfill after fix
```

Not:

```plaintext
Continue processing bad data
```

---

# Operational Thinking

Suppose:

```plaintext
Normal runtime = 20 min
```

Today:

```plaintext
Runtime = 3 hours
```

Questions to ask:

### Monitoring

```plaintext
Why is runtime abnormal?
```

### Timeout

```plaintext
Should task have been killed earlier?
```

### Logs

```plaintext
What was the task doing?
```

### Retry

```plaintext
Was the failure transient?
```

### Alerting

```plaintext
Who needs to be notified?
```

---

# Key Takeaways

```plaintext
Retries
=
Recover from temporary failures

Retry Delay
=
Allow systems time to recover

Execution Timeout
=
Kill stuck tasks

Failure Propagation
=
Protect downstream systems

Logs
=
Primary debugging tool

all_success
=
Default trigger rule
```

---

# Biggest Lesson

```plaintext
A production pipeline is not one that never fails.

A production pipeline is one that fails safely and recovers predictably.
```

---

# Real Data Engineering Mapping

Today's concepts apply directly to:

```plaintext
Bronze → Silver → Gold pipelines

API ingestion

Spark jobs

Athena refreshes

Dashboard updates
```

The goal is not preventing all failures.

The goal is:

```plaintext
Detect
Recover
Protect
Alert
```

when failures occur.
