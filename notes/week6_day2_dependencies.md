# Week 6 Day 2 - Task Dependencies & Operators

## Goal

Understand how Airflow manages workflow execution through:

* Operators
* Dependencies
* Sequential execution
* Parallel execution
* Failure propagation
* Logs
* EmptyOperator

---

# Operators

An Operator represents a unit of work in Airflow.

Examples:

* `PythonOperator`
* `BashOperator`
* `EmptyOperator`
* `SparkSubmitOperator`

Today's exercises used:

```python
PythonOperator
```

to execute Python functions.

---

# Sequential Execution

Created a DAG:

```plaintext
extract
    ↓
validate
    ↓
load
```

Code:

```python
extract_task >> validate_task >> load_task
```

Meaning:

* `validate` depends on `extract`
* `load` depends on `validate`

Execution order:

```plaintext
extract
    ↓
validate
    ↓
load
```

A downstream task only runs after all required upstream tasks succeed.

---

# Failure Propagation

Modified:

```python
def validate():
    raise Exception("Validation failed")
```

Observed:

```plaintext
extract
✅ Success

validate
❌ Failed

load
⛔ Upstream Failed
```

Key learning:

Airflow prevents downstream tasks from consuming data that has not successfully passed validation.

---

# Logs

Used task logs to investigate failures.

Found:

```plaintext
Validation failed
```

inside the validate task logs.

Logs are the primary debugging mechanism in Airflow.

---

# Parallel Execution

Created a DAG:

```plaintext
           extract
          /       \
validate_customer validate_shipment
          \       /
             load
```

Code:

```python
extract_task >> [customer_task, shipment_task]

[customer_task, shipment_task] >> load_task
```

Alternative syntax:

```python
extract_task >> [customer_task, shipment_task] >> load_task
```

Both create the same dependency graph.

---

# Fan-Out Pattern

One task triggers multiple downstream tasks.

Example:

```plaintext
extract
   ↓
customer
shipment
```

After `extract` succeeds, both validation tasks become runnable.

---

# Fan-In Pattern

Multiple tasks converge into a single downstream task.

Example:

```plaintext
customer
    ↓

    load

    ↑
shipment
```

`load` waits for **all** upstream dependencies to succeed.

---

# EmptyOperator

Added:

```python
from airflow.operators.empty import EmptyOperator

start = EmptyOperator(task_id="start")
end = EmptyOperator(task_id="end")
```

Example DAG:

```plaintext
start
   ↓
extract
   ↓
validate
   ↓
load
   ↓
end
```

Purpose:

* Improve DAG readability
* Create logical workflow boundaries
* Make large DAGs easier to understand

---

# Airflow Execution Model

Airflow does not execute tasks based on Python code order.

Airflow executes tasks based on dependency rules.

Think:

```plaintext
Given this dependency graph,
what tasks are allowed to run next?
```

---

# Real Data Engineering Mapping

Today's DAG:

```plaintext
extract
↓
validate
↓
load
```

maps to real workflows such as:

```plaintext
read_bronze
↓
validate_data
↓
build_silver
```

or

```plaintext
build_silver
↓
build_gold
↓
refresh_dashboard
```

The same dependency model applies.

---

# Key Takeaways

```plaintext
Operator
=
Unit of work

Dependency
=
Execution rule

Fan-Out
=
One task → many tasks

Fan-In
=
Many tasks → one task

Logs
=
Primary debugging tool

Upstream Failed
=
Downstream task blocked because dependency failed
```

---

# Biggest Lesson

Airflow does not think in terms of code execution order.

Airflow thinks in terms of dependency graphs.

Its job is to determine:

```plaintext
What can safely run next?
```

based on the dependency graph and task states.

---