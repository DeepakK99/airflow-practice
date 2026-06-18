# Week 6 Day 1

# Airflow Setup and First DAG

---

# Goal

Set up Apache Airflow locally using Docker and understand the fundamental execution model of Airflow.

By the end of the day:

* Airflow running locally
* Able to access UI
* Created first DAG
* Triggered DAG manually
* Viewed task logs
* Understood DAGs, DAG Runs, Tasks, and Task Instances

---

# Repository Structure

```plaintext
airflow-practice/

├── dags/
├── logs/
├── plugins/
├── docker-compose.yaml
├── notes/
```

---

# Airflow Deployment

Used Docker Compose to run Airflow locally.

Main services:

```plaintext
airflow-webserver
airflow-scheduler
airflow-worker
airflow-triggerer
postgres
redis
```

---

# Purpose of Each Component

## Webserver

Provides:

```plaintext
http://localhost:8080
```

Used for:

* DAG management
* Monitoring
* Logs
* Graph view

---

## Scheduler

Most important Airflow component.

Responsibilities:

* Reads DAG files
* Creates DAG Runs
* Schedules Task Instances
* Tracks dependencies

Without the scheduler:

```plaintext
DAG exists
```

but

```plaintext
Nothing executes
```

---

## Worker

Executes tasks.

Example:

```python
print("Hello Airflow")
```

runs on a worker.

---

## Postgres

Stores Airflow metadata.

Examples:

```plaintext
DAG Runs
Task Instances
Connections
Variables
Execution State
```

Does NOT store pipeline data.

---

## Redis

Used for communication between Airflow components.

---

# Airflow Initialization

First command:

```bash
docker compose up airflow-init
```

Purpose:

* Create metadata database
* Initialize Airflow tables
* Create default user
* Prepare environment

---

Important:

```plaintext
airflow-init
```

is a one-time setup service.

Successful completion usually shows:

```plaintext
Exited (0)
```

which means:

```plaintext
Success
```

not failure.

---

After initialization:

```bash
docker compose up -d
```

starts Airflow services.

---

# First DAG

File:

```plaintext
dags/hello_airflow.py
```

Created a simple DAG with one task:

```plaintext
hello_task
```

which prints:

```plaintext
Hello from Airflow
```

---

# Key Airflow Concepts

## DAG

Definition:

```plaintext
Blueprint of a workflow
```

Example:

```plaintext
Shipment Pipeline
```

A DAG defines:

* Tasks
* Dependencies
* Schedule

A DAG itself does not execute.

---

## DAG Run

Definition:

```plaintext
One execution of a DAG
```

Example:

```plaintext
Shipment Pipeline
run on a specific date/time
```

Multiple DAG Runs can exist for the same DAG.

---

## Task

Definition:

```plaintext
A unit of work
```

Example:

```plaintext
build_silver
```

A task is only a definition.

---

## Task Instance

Definition:

```plaintext
Execution of a task
within a specific DAG Run
```

Example:

```plaintext
build_silver
run on 2026-06-18
```

Task Instance is the actual execution.

---

# Airflow Execution Flow

Actual execution model:

```plaintext
Python DAG File
        ↓

Scheduler Reads DAG
        ↓

Creates DAG Run
        ↓

Creates Task Instance
        ↓

Worker Executes Task
        ↓

Logs Generated
        ↓

Success / Failure Recorded
```

This is how Airflow thinks.

---

# DAG Parameters

## dag_id

Unique workflow identifier.

Example:

```plaintext
hello_airflow
```

---

## start_date

Earliest date Airflow can consider for scheduling.

Will become important when learning catchup and backfills.

---

## schedule=None

Meaning:

```plaintext
Manual execution only
```

---

## catchup=False

Meaning:

```plaintext
Do not create historical runs automatically
```

Will become important later for backfills.

---

# UI Observations

Important areas explored:

## DAG List

Shows:

* DAG name
* Last run
* Schedule
* Status

---

## Graph View

Visual representation of workflow dependencies.

For first DAG:

```plaintext
hello_task
```

appears as a node.

---

## Logs

Logs show:

* Task execution
* Output
* Errors
* Success state

Used for debugging.

---

# Stretch DAG

Created:

```plaintext
extract
validate
load
```

Dependencies:

```plaintext
extract
    ↓
validate
    ↓
load
```

using:

```python
extract >> validate >> load
```

---

# Important Realization

Airflow is not simply:

```plaintext
Run Python Script
```

Airflow is:

```plaintext
Define Workflow
↓
Schedule Workflow
↓
Execute Tasks
↓
Track State
↓
Monitor Runs
```

It is an orchestration platform.

---

# Docker Commands Used

View running containers:

```bash
docker ps
```

---

View scheduler logs:

```bash
docker compose logs -f airflow-scheduler
```

---

View webserver logs:

```bash
docker compose logs -f airflow-webserver
```

---

Stop Airflow:

```bash
docker compose down
```

---

# Biggest Takeaways

```plaintext
DAG
=
Blueprint

DAG Run
=
One execution

Task
=
Definition of work

Task Instance
=
Actual execution

Scheduler
=
Brain

Worker
=
Execution Engine

Airflow
=
Workflow Orchestrator
```

---

# What Surprised Me

* Airflow consists of multiple services, not a single application.
* Scheduler is the core component responsible for execution.
* DAGs and DAG Runs are different concepts.
* Tasks and Task Instances are different concepts.
* Airflow stores workflow metadata in Postgres.
* airflow-init is only a one-time initialization step.

---
