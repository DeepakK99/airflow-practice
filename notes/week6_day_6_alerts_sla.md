# Week 6 Day 6

# Notifications, Alerts, SLAs & Operational Ownership

## Goal

Learn how production pipelines are operated after deployment.

By the end of today:

* Understood ownership
* Understood stakeholders and consumers
* Learned SLA thinking
* Understood alerting concepts
* Learned runbook design
* Practiced production incident response

---

# Key Mindset Shift

A pipeline is not complete when:

```plaintext
Code works
```

A pipeline is complete when:

```plaintext
Code works
+
Failures are visible
+
Ownership is clear
+
Recovery is documented
```

---

# Ownership

Every production pipeline should have an owner.

Example:

```plaintext
Shipment Analytics Pipeline
```

Owner:

```plaintext
Data Engineering Team
```

Responsibilities:

```plaintext
Monitor pipeline health

Investigate failures

Perform backfills

Maintain SLA compliance

Deploy fixes
```

---

# Business Stakeholders

Stakeholders are the people who care about the outcome of the pipeline.

Examples:

```plaintext
Operations Managers

Logistics Managers

Supply Chain Teams

Regional Sales Teams
```

They are not responsible for fixing failures.

They care about:

```plaintext
Reliable and timely analytics
```

---

# Downstream Consumers

Consumers directly use the output data.

Examples:

```plaintext
Power BI Dashboards

Analysts

Reports

Data Products
```

These systems depend on successful pipeline execution.

---

# Why Ownership Matters

Question:

```plaintext
Pipeline fails at 2:15 AM

Who fixes it?
```

Without ownership:

```plaintext
Nobody knows
Nobody acts
```

With ownership:

```plaintext
Alert fires
↓
Owner notified
↓
Investigation starts
```

---

# Default Args

Introduced:

```python
default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}
```

Used in:

```python
with DAG(
    dag_id="shipment_pipeline",
    default_args=default_args,
)
```

---

# Why Use default_args

Without default_args:

```plaintext
retries
retry_delay
owner
```

must be repeated for every task.

Example:

```plaintext
20 tasks
↓
20 duplicate configurations
```

---

Benefits:

```plaintext
Centralized configuration

Less duplication

Easier maintenance
```

Example:

```plaintext
Change retries from 2 to 3
```

Update once instead of updating every task.

---

# SLA Thinking

Example requirement:

```plaintext
Dashboard ready by 8:00 AM
```

Pipeline:

```plaintext
Starts: 2:00 AM
Finishes: 3:00 AM
Dashboard: 3:10 AM
```

Result:

```plaintext
SLA Met
```

---

Scenario:

```plaintext
Pipeline finishes: 9:00 AM
Dashboard refreshes: 9:15 AM
```

Result:

```plaintext
SLA Missed
```

---

# Important Lesson

Pipeline status:

```plaintext
Success
```

does NOT automatically mean:

```plaintext
Business Success
```

A pipeline can:

```plaintext
Complete successfully
```

and still be:

```plaintext
Business failure
```

if the SLA is missed.

---

# Technical Success vs Business Success

Technical Success:

```plaintext
All Airflow tasks green
```

---

Business Success:

```plaintext
Dashboard available before SLA deadline
```

Both matter.

---

# Monitoring vs Data Quality vs SLA

Understanding the distinction:

---

## Operational Monitoring

Answers:

```plaintext
Is the pipeline behaving normally?
```

Examples:

```plaintext
Runtime spikes

Task failures

Excessive retries

Infrastructure issues
```

---

## Data Quality

Answers:

```plaintext
Is the data correct?
```

Examples:

```plaintext
Revenue = 0

Negative shipment cost

Missing records

Unexpected row counts
```

---

## SLA Monitoring

Answers:

```plaintext
Will business receive data on time?
```

Examples:

```plaintext
Late dashboard refresh

Pipeline exceeds deadline
```

---

# Example Scenarios

Scenario:

```plaintext
Revenue = 0

Pipeline succeeded
```

Classification:

```plaintext
Data Quality Issue
```

Monitoring should detect it.

---

Scenario:

```plaintext
build_gold normally takes 20 min

Today takes 3 hours
```

Classification:

```plaintext
Operational Monitoring Issue
```

Potentially:

```plaintext
SLA Issue
```

if delivery becomes late.

---

# DAG Documentation

Every production DAG should contain:

```plaintext
Purpose

Inputs

Outputs

Owner

SLA

Recovery Process
```

Example DAG description:

```python
description="Processes shipment data through Bronze, Silver and Gold layers"
```

---

# Runbooks

Definition:

```plaintext
Document describing how to respond to failures
```

Purpose:

```plaintext
Reduce investigation time

Provide consistent recovery steps

Help on-call engineers
```

---

# Example Runbook

Issue:

```plaintext
silver_quality_check failed
```

---

## Step 1

Identify failing task.

```plaintext
Airflow Graph View
```

---

## Step 2

Inspect logs.

Questions:

```plaintext
What failed?

When?

Which validation rule?
```

---

## Step 3

Trace lineage.

Example:

```plaintext
silver_quality_check
       ↑
build_silver
       ↑
bronze_validation
       ↑
extract_shipment
```

Determine where bad data originated.

---

## Step 4

Identify root cause.

Examples:

```plaintext
Schema change

Bad source data

Transformation bug

Missing file
```

---

## Step 5

Apply fix.

Examples:

```plaintext
Code fix

Data correction

Configuration update
```

---

## Step 6

Reprocess.

Options:

```plaintext
Retry task

Backfill DAG
```

---

## Step 7

Validate recovery.

Confirm:

```plaintext
Silver valid

Gold valid

Metrics generated

Dashboard refreshed
```

---

## Step 8

Prevent recurrence.

Questions:

```plaintext
Should monitoring be improved?

Should a new quality rule be added?

Should documentation be updated?
```

---

# Operational Maturity Levels

Level 1:

```plaintext
Pipeline Exists
```

---

Level 2:

```plaintext
Pipeline Monitored
```

---

Level 3:

```plaintext
Pipeline Alerted
```

---

Level 4:

```plaintext
Pipeline Documented
```

---

Level 5:

```plaintext
Pipeline Recoverable
```

---

# Production Incident Flow

Example:

```plaintext
silver_quality_check fails
```

Expected process:

```plaintext
Alert
↓
Owner notified
↓
Logs reviewed
↓
Lineage traced
↓
Root cause identified
↓
Fix deployed
↓
Backfill executed
↓
Validation completed
```

---

# Concepts Connected Today

Today connected several topics learned earlier:

```plaintext
Monitoring
↓
Alerting
↓
Ownership
↓
Lineage
↓
Observability
↓
Runbooks
↓
Backfills
```

Instead of isolated concepts, they now form an operational workflow.

---

# Key Takeaways

```plaintext
Owner
=
Who fixes failures

Stakeholder
=
Who cares about the outcome

Consumer
=
Who uses the data

SLA
=
Business deadline

Monitoring
=
Detect problems

Alerting
=
Notify owners

Runbook
=
Recovery instructions
```

---

# Biggest Lesson

```plaintext
Building a pipeline is only half the job.

Operating, monitoring, documenting and recovering the pipeline is what makes it production-ready.
```

---

# Real Data Engineering Mapping

A mature pipeline should have:

```plaintext
Airflow DAG

Monitoring

Alerting

Ownership

Documentation

Runbooks

Backfill Strategy
```

Not just:

```plaintext
Working code
```

because production systems are judged by:

```plaintext
Reliability

Recoverability

Business outcomes
```

not only technical correctness.
